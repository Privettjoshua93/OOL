from django.core.mail import send_mail
from django.contrib.auth.models import User, Group

def get_user_emails_by_group(group_name):
    group = Group.objects.get(name=group_name)
    return [user.email for user in group.user_set.all()]

def send_email(subject, message, recipient_list):
    send_mail(subject, message, 'testing@onoffloa.onmicrosoft.com', recipient_list)