from django.core.mail import EmailMultiAlternatives, get_connection
from django.contrib.auth.models import Group
from .models import AzureCredentials

def get_user_emails_by_group(group_name):
    group = Group.objects.get(name=group_name)
    return [user.email for user in group.user_set.all()]

def send_email(subject, details_dict, recipient_list):
    """
    Send an email with the provided details.

    :param subject: Subject of the email.
    :param details_dict: Dictionary containing the details to include in the email.
    :param recipient_list: List of recipient email addresses.
    """
    credentials = AzureCredentials.objects.first()
    if credentials:
        EMAIL_HOST = credentials.smtp_host
        EMAIL_PORT = credentials.smtp_port
        EMAIL_HOST_USER = credentials.smtp_user
        EMAIL_HOST_PASSWORD = credentials.smtp_password  # Decryption is handled by EncryptedCharField
        EMAIL_USE_TLS = True
        EMAIL_USE_SSL = False

        # Format the details into the email message
        message = "\n".join([f"{key}: {value}" for key, value in details_dict.items()])

        email = EmailMultiAlternatives(
            subject, message, EMAIL_HOST_USER, recipient_list,
            connection=get_connection(
                host=EMAIL_HOST,
                port=EMAIL_PORT,
                username=EMAIL_HOST_USER,
                password=EMAIL_HOST_PASSWORD,  # Decrypt for use
                use_tls=EMAIL_USE_TLS,
                use_ssl=EMAIL_USE_SSL
            )
        )
        email.send(fail_silently=False)