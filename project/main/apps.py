from django.apps import AppConfig
from django.conf import settings

class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        from .models import AzureCredentials

        def update_social_auth_settings():
            credentials = AzureCredentials.objects.first()
            if credentials:
                settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY = credentials.client_id
                settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET = credentials.client_secret
                settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID = credentials.tenant_id
                
        update_social_auth_settings()