from django import forms
from .models import Onboarding, Offboarding, LOA, AzureCredentials

class OnboardingForm(forms.ModelForm):
    class Meta:
        model = Onboarding
        fields = [
            'first_name', 'last_name', 'preferred_work_email', 'personal_email',
            'mobile_number', 'title', 'manager', 'department', 'mac_or_pc',
            'start_date', 'location', 'groups', 'distribution_lists', 'shared_drives'
        ]

class OffboardingForm(forms.ModelForm):
    class Meta:
        model = Offboarding
        fields = ['first_name', 'last_name', 'last_date_time', 'additional_notes']

class OffboardingAdminForm(forms.ModelForm):
    class Meta:
        model = Offboarding
        fields = ['first_name', 'last_name', 'last_date_time', 'additional_notes', 'status']

class OnboardingAdminForm(forms.ModelForm):
    class Meta:
        model = Onboarding
        fields = [
            'first_name', 'last_name', 'preferred_work_email', 'personal_email',
            'mobile_number', 'title', 'manager', 'department', 'mac_or_pc',
            'start_date', 'location', 'groups', 'distribution_lists', 'shared_drives', 'status'
        ]

class LOAForm(forms.ModelForm):
    class Meta:
        model = LOA
        fields = ['start_date', 'end_date', 'last_date']  # Include last_date

class LOAAdminForm(forms.ModelForm):
    class Meta:
        model = LOA
        fields = ['start_date', 'end_date', 'last_date', 'status']  # Include last_date

class AzureCredentialsForm(forms.ModelForm):
    email_use_tls = forms.BooleanField(required=False)
    email_use_ssl = forms.BooleanField(required=False)
    
    class Meta:
        model = AzureCredentials
        fields = [
            'client_id', 'tenant_id', 'client_secret',
            'smtp_host', 'smtp_port', 'smtp_user', 'smtp_password',
            'email_use_tls', 'email_use_ssl'
        ]