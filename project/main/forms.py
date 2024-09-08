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
            'storage_account_name', 'container_name',
            'email_use_tls', 'email_use_ssl'
        ]

class DynamicOnboardingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        fields_queryset = kwargs.pop('fields_queryset', None)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if fields_queryset:
            for field in fields_queryset:
                field_key = f'field_{field.id}'
                self.fields[field_key] = self.create_form_field(field)

    def create_form_field(self, field):
        if field.field_type == 'text':
            return forms.CharField(label=field.label, required=field.is_active)
        elif field.field_type == 'email':
            return forms.EmailField(label=field.label, required=field.is_active)
        elif field.field_type == 'number':
            return forms.CharField(label=field.label, required=field.is_active)
        elif field.field_type == 'date':
            return forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label=field.label, required=field.is_active)
        elif field.field_type == 'datetime':
            return forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'datetime-local'}), label=field.label, required=field.is_active)
        elif field.field_type == 'textarea':
            return forms.CharField(widget=forms.Textarea, label=field.label, required=field.is_active)
        elif field.field_type == 'dropdown':
            options = field.options.split(',')
            return forms.ChoiceField(choices=[(option, option) for option in options], label=field.label, required=field.is_active)
        else:
            return forms.CharField(label=field.label, required=field.is_active)

class OnboardingAdminForm(forms.ModelForm):
    status = forms.ChoiceField(choices=[('Pending', 'Pending'), ('Complete', 'Complete')])
    class Meta:
        model = Onboarding
        fields = ['user', 'field_data', 'status']

class OnboardingForm(forms.ModelForm):
    class Meta:
        model = Onboarding
        fields = ['user', 'field_data', 'status']