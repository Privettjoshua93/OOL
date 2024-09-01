from django import forms
from .models import Onboarding, Offboarding, LOA

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

class LOAForm(forms.ModelForm):
    class Meta:
        model = LOA
        fields = ['start_date', 'end_date']

class LOAAdminForm(forms.ModelForm):
    class Meta:
        model = LOA
        fields = ['start_date', 'end_date', 'status']