from django.db import models

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