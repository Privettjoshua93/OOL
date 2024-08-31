from django import forms
from .models import Onboarding, Offboarding, LOA

class OnboardingForm(forms.ModelForm):
    class Meta:
        model = Onboarding
        fields = ['employee_name', 'start_date', 'status', 'details']

class OffboardingForm(forms.ModelForm):
    class Meta:
        model = Offboarding
        fields = ['employee_name', 'end_date', 'status', 'details']

class LOAForm(forms.ModelForm):
    class Meta:
        model = LOA
        fields = ['start_date', 'end_date']

class LOAAdminForm(forms.ModelForm):
    class Meta:
        model = LOA
        fields = ['start_date', 'end_date', 'status']