from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedCharField

class Onboarding(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Complete', 'Complete'),
    ]

    MAC_OR_PC_CHOICES = [
        ('Mac', 'Mac'),
        ('PC', 'PC'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    preferred_work_email = models.EmailField(max_length=100)
    personal_email = models.EmailField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    title = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    mac_or_pc = models.CharField(max_length=3, choices=MAC_OR_PC_CHOICES)
    start_date = models.DateField()
    location = models.CharField(max_length=100)
    groups = models.TextField()
    distribution_lists = models.TextField()
    shared_drives = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    details = models.TextField(default='')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.status}'

class Offboarding(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Complete', 'Complete'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    last_date_time = models.DateTimeField()
    additional_notes = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    details = models.TextField(default='')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.status}'
    
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
    client_id = EncryptedCharField(max_length=100)
    tenant_id = EncryptedCharField(max_length=100)
    client_secret = EncryptedCharField(max_length=100)

    def __str__(self):
        return "Azure Credentials"