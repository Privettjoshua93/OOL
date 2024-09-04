from django.core.mail import send_mail, get_connection
from django.contrib.auth.models import User, Group
from .models import AzureCredentials

def get_user_emails_by_group(group_name):
    group = Group.objects.get(name=group_name)
    return [user.email for user in group.user_set.all()]

def send_email(subject, message, recipient_list):
    credentials = AzureCredentials.objects.first()
    if credentials:
        EMAIL_HOST = credentials.smtp_host
        EMAIL_PORT = credentials.smtp_port
        EMAIL_HOST_USER = credentials.smtp_user
        EMAIL_HOST_PASSWORD = credentials.smtp_password  # Decryption is handled by EncryptedCharField
        EMAIL_USE_TLS = True
        EMAIL_USE_SSL = False

        send_mail(subject, message, EMAIL_HOST_USER, recipient_list,
                  fail_silently=False,
                  auth_user=EMAIL_HOST_USER,
                  auth_password=credentials.smtp_password,  # Decrypt for use
                  connection=get_connection(
                      host=EMAIL_HOST,
                      port=EMAIL_PORT,
                      username=EMAIL_HOST_USER,
                      password=EMAIL_HOST_PASSWORD,  # Decrypt for use
                      use_tls=EMAIL_USE_TLS,
                      use_ssl=EMAIL_USE_SSL
                  ))