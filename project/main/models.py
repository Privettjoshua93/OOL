from django.db import models
from django.contrib.auth.models import User

class Onboarding(models.Model):
    employee_name = models.CharField(max_length=100)
    start_date = models.DateField()
    status = models.CharField(max_length=50, default='Pending')
    details = models.TextField()

    def __str__(self):
        return f'{self.employee_name} - {self.status}'

class Offboarding(models.Model):
    employee_name = models.CharField(max_length=100)
    end_date = models.DateField()
    status = models.CharField(max_length=50, default='Pending')
    details = models.TextField()

    def __str__(self):
        return f'{self.employee_name} - {self.status}'
    
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