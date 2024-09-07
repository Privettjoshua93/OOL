from django.utils.deprecation import MiddlewareMixin
from main.models import AzureCredentials
from datetime import datetime, timedelta
import os
from django.conf import settings
from django.core.management import call_command

class CheckBackupMiddleware(MiddlewareMixin):
    def process_request(self, request):
        backup_file = os.path.join(settings.BASE_DIR, 'last_backup.txt')
        now = datetime.now()  # Current time

        if os.path.exists(backup_file):
            with open(backup_file, 'r') as file:
                last_backup = datetime.fromisoformat(file.read().strip())
        else:
            last_backup = now - timedelta(days=1)  # Set to 24 hours ago if file doesn't exist

        if now - last_backup >= timedelta(days=1):
            call_command('backup_db')  # Execute backup_db command
            with open(backup_file, 'w') as file:
                file.write(now.isoformat())

class UpdateSocialAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        from django.conf import settings
        credentials = AzureCredentials.objects.first()
        if credentials:
            settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY = credentials.client_id
            settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET = credentials.client_secret
            settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID = credentials.tenant_id