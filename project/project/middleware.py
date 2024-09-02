from django.utils.deprecation import MiddlewareMixin
from main.models import AzureCredentials

class UpdateSocialAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        from django.conf import settings
        credentials = AzureCredentials.objects.first()
        if credentials:
            settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY = credentials.client_id
            settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET = credentials.client_secret
            settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID = credentials.tenant_id