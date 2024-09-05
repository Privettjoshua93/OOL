from django import forms
from .models import Onboarding, Offboarding, LOA, AzureCredentials, OnboardingField

class OffboardingForm(forms.ModelForm):
    class Meta:
        model = Offboarding
        fields = ['first_name', 'last_name', 'last_date_time', 'additional_notes']

class OffboardingAdminForm(forms.ModelForm):
    class Meta:
        model = Offboarding
        fields = ['first_name', 'last_name', 'last_date_time', 'additional_notes', 'status']

class LOAForm(forms.ModelForm):
    class Meta:
        model = LOA
        fields = ['start_date', 'end_date']

class LOAAdminForm(forms.ModelForm):
    class Meta:
        model = LOA
        fields = ['start_date', 'end_date', 'status']

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

class DynamicOnboardingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        fields_queryset = kwargs.pop('fields_queryset', None)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if fields_queryset:
            for field in fields_queryset:
                if field.field_type == 'text':
                    self.fields[f'field_{field.id}'] = forms.CharField(label=field.label, required=field.is_active)
                elif field.field_type == 'email':
                    self.fields[f'field_{field.id}'] = forms.EmailField(label=field.label, required=field.is_active)
                elif field.field_type == 'number':
                    self.fields[f'field_{field.id}'] = forms.CharField(label=field.label, required=field.is_active)
                elif field.field_type == 'date':
                    self.fields[f'field_{field.id}'] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label=field.label, required=field.is_active)
                elif field.field_type == 'datetime':
                    self.fields[f'field_{field.id}'] = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'datetime-local'}), label=field.label, required=field.is_active)
                elif field.field_type == 'textarea':
                    self.fields[f'field_{field.id}'] = forms.CharField(widget=forms.Textarea, label=field.label, required=field.is_active)
                elif field.field_type == 'dropdown':
                    options = field.options.split(',')
                    self.fields[f'field_{field.id}'] = forms.ChoiceField(choices=[(option, option) for option in options], label=field.label, required=field.is_active)

class OnboardingAdminForm(forms.ModelForm):
    status = forms.ChoiceField(choices=[('Pending', 'Pending'), ('Complete', 'Complete')])
    class Meta:
        model = Onboarding
        fields = ['user', 'field_data', 'status']