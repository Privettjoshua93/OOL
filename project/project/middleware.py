from django.utils.deprecation import MiddlewareMixin
from main.models import AzureCredentials
from datetime import datetime, timedelta
import os
from django.conf import settings
from django.core.management import call_command
import mmap

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

class DynamicKeyMiddleware(MiddlewareMixin):
    def fetch_key_from_azure(self):
        credentials = AzureCredentials.objects.first()
        if not credentials or credentials.vault_name in ['vault name', '']:
            return None  # Return gracefully if no valid Azure credentials found

        # Setup Azure Key Vault credentials if they exist
        try:
            credential = ClientSecretCredential(
                tenant_id=credentials.tenant_id,
                client_id=credentials.client_id,
                client_secret=credentials.client_secret
            )
            key_client = KeyClient(vault_url=f"https://{credentials.vault_name}.vault.azure.net", credential=credential)
            key = key_client.get_key(credentials.key_name)

            key_value = key.key.n.to_bytes((key.key.n.bit_length() + 7) // 8, byteorder='big')
            encryption_key = base64.urlsafe_b64encode(key_value[:32]).decode('utf-8')

            # Store key in memory-mapped file
            with open('dynamic_key', 'r+b') as f:
                mm = mmap.mmap(f.fileno(), 0)
                mm.seek(0)
                mm.write(encryption_key.encode('utf-8'))
                mm.seek(0)
        except Exception as e:
            print(f"Failed to fetch key from Azure: {str(e)}")

    def process_request(self, request):
        try:
            with open('dynamic_key', 'r+b') as f:
                mm = mmap.mmap(f.fileno(), 0)
                mm.seek(0)
                settings.FIELD_ENCRYPTION_KEY = mm.read(64).rstrip(b'\0').decode('utf-8')
        except FileNotFoundError:
            # Generate new temporary key and store it in RAM
            self.fetch_key_from_azure()
            try:
                with open('dynamic_key', 'r+b') as f:
                    mm = mmap.mmap(f.fileno(), 0)
                    mm.seek(0)
                    settings.FIELD_ENCRYPTION_KEY = mm.read(64).rstrip(b'\0').decode('utf-8')
            except FileNotFoundError:
                # Handle this as a soft error; it will fail if encryption is needed but not block access
                settings.FIELD_ENCRYPTION_KEY = None

    def process_view(self, request, view_func, view_args, view_kwargs):
        current_key = settings.FIELD_ENCRYPTION_KEY
        if current_key:
            # Fetch a new key dynamically and overwrite the existing key in RAM
            self.fetch_key_from_azure()