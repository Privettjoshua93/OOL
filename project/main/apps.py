from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.conf import settings

class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        from .models import AzureCredentials

        def update_social_auth_settings(**kwargs):
            credentials = AzureCredentials.objects.first()
            if credentials:
                settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY = credentials.client_id
                settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET = credentials.client_secret
                settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID = credentials.tenant_id
    
                # Update SMTP settings
                settings.EMAIL_HOST = credentials.smtp_host
                settings.EMAIL_PORT = credentials.smtp_port
                settings.EMAIL_HOST_USER = credentials.smtp_user
                settings.EMAIL_HOST_PASSWORD = credentials.smtp_password  # Decryption handled by EncryptedCharField
                settings.DEFAULT_FROM_EMAIL = credentials.smtp_user  # Optional, if you want to set the default from email

        post_migrate.connect(update_social_auth_settings, sender=self)