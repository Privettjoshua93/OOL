import os
import base64
from pathlib import Path
from django.conf import settings
from azure.identity import ClientSecretCredential
from azure.keyvault.keys import KeyClient
import mmap
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ubxmhpn_*l^4*j1l*y!bjo$t+68b-k+l+-mce^i%_dj5x%3_rx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Hosts the server will respond to
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',

    # Third-party apps
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'social_django',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    ]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'project.middleware.UpdateSocialAuthMiddleware',
    'project.middleware.CheckBackupMiddleware',
    
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),  # Correctly format BASE_DIR for concatenation
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/topics/auth/passwords/

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# Default auto field
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Enable local user authentication
    'allauth.account.auth_backends.AuthenticationBackend',
    'social_core.backends.azuread_tenant.AzureADTenantOAuth2',  # Enable Microsoft SSO
)

def update_social_auth_settings():
    from main.models import AzureCredentials
    credentials = AzureCredentials.objects.first()
    if credentials:
        settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY = credentials.client_id
        settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET = credentials.client_secret
        settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID = credentials.tenant_id


# Social Auth Configuration
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/login_redirect/'  # This URL will handle the redirect logic post-login
LOGOUT_REDIRECT_URL = '/'
SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SCOPE = ['User.Read']
SOCIAL_AUTH_URL_NAMESPACE = 'social'


# Ensure that these settings are correctly populated from the database
SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY = ""
SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET = ""
SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID = ""

# Add necessary allauth settings
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = False

# Changes might include additional SSO settings if needed
SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',  # Check and associate by email
    'social_core.pipeline.user.create_user',
    'main.views.custom_save_user_in_pipeline',  # Custom step to save additional details
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)


def fetch_encryption_key_from_ram():
    try:
        with open('dynamic_key', 'r+b') as f:
            mm = mmap.mmap(f.fileno(), 0)
            mm.seek(0)
            return mm.read(64).rstrip(b'\0').decode('utf-8')
    except FileNotFoundError:
        # Generate a temporary key if dynamic_key file is missing
        temp_key = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')
        with open('dynamic_key', 'wb') as f:
            f.write(b'\0' * 64)
        with open('dynamic_key', 'r+b') as f:
            mm = mmap.mmap(f.fileno(), 0)
            mm.seek(0)
            mm.write(temp_key.encode('utf-8'))
            mm.seek(0)
        return temp_key

# Initially set the FIELD_ENCRYPTION_KEY
FIELD_ENCRYPTION_KEY = config('ENCRYPTION_KEY')

def fetch_encryption_key_from_azure():
    credentials = AzureCredentials.objects.first()
    if not credentials:
        raise ValueError("No Azure Credentials found")
    
    credential = ClientSecretCredential(
        tenant_id=credentials.tenant_id,
        client_id=credentials.client_id,
        client_secret=credentials.client_secret
    )
    key_client = KeyClient(vault_url=f"https://{credentials.vault_name}.vault.azure.net", credential=credential)
    key = key_client.get_key(credentials.key_name)
    
    key_value = key.key.n
    encryption_key = base64.urlsafe_b64encode(key_value[:32]).decode('utf-8')
    with open('/dev/shm/dynamic_key', 'w+') as f:
        f.seek(0)
        f.write(encryption_key)
        f.truncate()