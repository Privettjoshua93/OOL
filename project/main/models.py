from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedCharField
from django.utils import timezone
from django import forms

class OnboardingField(models.Model):
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=50, choices=[
        ('text', 'Single Line of Text'),
        ('textarea', 'Multiple Lines of Text'),
        ('email', 'Email'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('datetime', 'Date/Time'),
        ('dropdown', 'Dropdown')
    ])
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    options = models.TextField(blank=True, help_text="Comma-separated options for dropdown fields.")

    def __str__(self):
        return self.label

    class Meta:
        ordering = ['order']

def populate_default_fields():
    initial_fields = [
        {'label': 'First Name', 'field_type': 'text', 'is_active': True, 'order': 1},
        {'label': 'Last Name', 'field_type': 'text', 'is_active': True, 'order': 2},
        {'label': 'Preferred Work Email', 'field_type': 'email', 'is_active': True, 'order': 3},
        {'label': 'Personal Email', 'field_type': 'email', 'is_active': True, 'order': 4},
        {'label': 'Mobile Number', 'field_type': 'text', 'is_active': True, 'order': 5},
        {'label': 'Title', 'field_type': 'text', 'is_active': True, 'order': 6},
        {'label': 'Manager', 'field_type': 'text', 'is_active': True, 'order': 7},
        {'label': 'Department', 'field_type': 'text', 'is_active': True, 'order': 8},
        {'label': 'Mac or PC', 'field_type': 'dropdown', 'is_active': True, 'order': 9, 'options': 'Mac,PC'},
        {'label': 'Start Date', 'field_type': 'date', 'is_active': True, 'order': 10},
        {'label': 'Location', 'field_type': 'text', 'is_active': True, 'order': 11},
        {'label': 'Groups', 'field_type': 'text', 'is_active': True, 'order': 12},
        {'label': 'Distribution Lists', 'field_type': 'textarea', 'is_active': True, 'order': 13},
        {'label': 'Shared Drives', 'field_type': 'textarea', 'is_active': True, 'order': 14},
    ]
    
    for field in initial_fields:
        OnboardingField.objects.get_or_create(label=field['label'], defaults=field)

class Onboarding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    field_data = models.JSONField(default=dict)  # Storing field data as JSON
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f'Onboarding for {self.user} - {self.status}'

def populate_default_fields():
    initial_fields = [
        {'label': 'First Name', 'field_type': 'text', 'is_active': True, 'order': 1},
        {'label': 'Last Name', 'field_type': 'text', 'is_active': True, 'order': 2},
        {'label': 'Preferred Work Email', 'field_type': 'email', 'is_active': True, 'order': 3},
        {'label': 'Personal Email', 'field_type': 'email', 'is_active': True, 'order': 4},
        {'label': 'Mobile Number', 'field_type': 'text', 'is_active': True, 'order': 5},
        {'label': 'Title', 'field_type': 'text', 'is_active': True, 'order': 6},
        {'label': 'Manager', 'field_type': 'text', 'is_active': True, 'order': 7},
        {'label': 'Department', 'field_type': 'text', 'is_active': True, 'order': 8},
        {'label': 'Mac or PC', 'field_type': 'dropdown', 'is_active': True, 'order': 9, 'options': 'Mac,PC'},
        {'label': 'Start Date', 'field_type': 'date', 'is_active': True, 'order': 10},
        {'label': 'Location', 'field_type': 'text', 'is_active': True, 'order': 11},
        {'label': 'Groups', 'field_type': 'text', 'is_active': True, 'order': 12},
        {'label': 'Distribution Lists', 'field_type': 'textarea', 'is_active': True, 'order': 13},
        {'label': 'Shared Drives', 'field_type': 'textarea', 'is_active': True, 'order': 14},
    ]

    for field in initial_fields:
        OnboardingField.objects.get_or_create(label=field['label'], defaults=field)

class Offboarding(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Complete', 'Complete'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    last_date_time = models.DateTimeField(default=timezone.now)
    additional_notes = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    details = models.TextField(default='')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.status}'
    
class OffboardingAdminForm(forms.ModelForm):
    class Meta:
        model = Offboarding
        fields = ['first_name', 'last_name', 'last_date_time', 'additional_notes', 'status']

class LOA(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Denied', 'Denied'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f'{self.user.username} - {self.status}'

class AzureCredentials(models.Model):
    client_id = models.CharField(max_length=100)
    tenant_id = models.CharField(max_length=100)
    client_secret = EncryptedCharField(max_length=100)  # Updated to be encrypted
    smtp_host = models.CharField(max_length=100, default='smtp.example.com')
    smtp_port = models.PositiveIntegerField(default=587)
    smtp_user = models.CharField(max_length=100, default='user@example.com')
    smtp_password = EncryptedCharField(max_length=100)  # Updated to be encrypted
    storage_account_name = models.CharField(max_length=100, default='default_storage_account')
    container_name = models.CharField(max_length=100, default='default_container')

    def __str__(self):
        return self.client_id