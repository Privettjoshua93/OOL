from .models import AzureCredentials
from .forms import AzureCredentialsForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Onboarding, Offboarding, LOA
from .forms import OnboardingForm, OffboardingForm, LOAForm, LOAAdminForm, OffboardingAdminForm, OnboardingAdminForm
import json
from social_django.utils import load_strategy
from .models import AzureCredentials
from .forms import AzureCredentialsForm

# Helper Functions for Access Control
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_approver(user):
    return user.groups.filter(name='Approver').exists()

def is_user(user):
    return user.groups.filter(name='User').exists()

def is_it(user):
    return user.groups.filter(name='IT').exists()

@login_required
def home_admin_hr(request):
    if is_it(request.user):
        return redirect('home_it')
    if not is_admin(request.user):
        return redirect('home_user')
    return render(request, 'home_admin_hr.html')

# User Home View
@login_required
def home_user(request):
    # If user is an approver, redirect to LOA admin overview
    if is_approver(request.user):
        return redirect('loa_admin_hr')
    return render(request, 'home_user.html')

@login_required
@user_passes_test(is_admin)
def onboarding(request):
    query = request.GET.get('q', '')
    if query:
        onboardings = Onboarding.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(status__icontains=query)
        )
    else:
        onboardings = Onboarding.objects.all()
    return render(request, 'onboarding.html', {'onboardings': onboardings, 'query': query})

@login_required
@user_passes_test(is_admin)
def onboarding_submission_overview(request):
    onboarding_id = request.GET.get('id')
    onboarding = get_object_or_404(Onboarding, id=onboarding_id)
    if request.method == 'POST':
        form = OnboardingAdminForm(request.POST, instance=onboarding)
        if form.is_valid():
            print("Form is valid!")
            print("Status before saving:", form.cleaned_data['status'])
            form.save()
            print("Saved Onboarding Status:", onboarding.status)
            return redirect('onboarding')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = OnboardingAdminForm(instance=onboarding)
    return render(request, 'onboarding_submission_overview.html', {'form': form, 'onboarding': onboarding})

@login_required
@user_passes_test(is_admin)
def new_onboarding(request):
    if request.method == 'POST':
        form = OnboardingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('onboarding')
    else:
        form = OnboardingForm()
    return render(request, 'new_onboarding.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_onboarding(request):
    onboarding_id = request.GET.get('id')
    onboarding = get_object_or_404(Onboarding, id=onboarding_id)
    if request.method == 'POST':
        form = OnboardingForm(request.POST, instance=onboarding)
        if form.is_valid():
            form.save()
            return redirect('onboarding')
    else:
        form = OnboardingForm(instance=onboarding)
    return render(request, 'new_onboarding.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_onboarding(request):
    onboarding_id = request.GET.get('id')
    onboarding = get_object_or_404(Onboarding, id=onboarding_id)
    onboarding.delete()
    return redirect('onboarding')

@login_required
@user_passes_test(is_admin)
def offboarding(request):
    query = request.GET.get('q', '')
    if query:
        offboardings = Offboarding.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(last_date_time__icontains=query) |
            Q(status__icontains=query)
        )
    else:
        offboardings = Offboarding.objects.all()
    return render(request, 'offboarding.html', {'offboardings': offboardings, 'query': query})

@login_required
@user_passes_test(is_admin)
def offboarding_submission_overview(request):
    offboarding_id = request.GET.get('id')
    offboarding = get_object_or_404(Offboarding, id=offboarding_id)
    if request.method == 'POST':
        form = OffboardingAdminForm(request.POST, instance=offboarding)
        if form.is_valid():
            form.save()
            return redirect('offboarding')
    else:
        form = OffboardingAdminForm(instance=offboarding)
    return render(request, 'offboarding_submission_overview.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def new_offboarding(request):
    if request.method == 'POST':
        form = OffboardingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('offboarding')
    else:
        form = OffboardingForm()
    return render(request, 'new_offboarding.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_offboarding(request):
    offboarding_id = request.GET.get('id')
    offboarding = get_object_or_404(Offboarding, id=offboarding_id)
    if request.method == 'POST':
        form = OffboardingForm(request.POST, instance=offboarding)
        if form.is_valid():
            form.save()
            return redirect('offboarding')
    else:
        form = OffboardingForm(instance=offboarding)
    return render(request, 'new_offboarding.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_offboarding(request):
    offboarding_id = request.GET.get('id')
    offboarding = get_object_or_404(Offboarding, id=offboarding_id)
    offboarding.delete()
    return redirect('offboarding')

# LOA Admin Overview View
@login_required
@user_passes_test(lambda u: is_admin(u) or is_approver(u))
def loa_admin_hr(request):
    query = request.GET.get('q', '')
    if query:
        loas = LOA.objects.filter(
            Q(user__username__icontains=query) |
            Q(status__icontains=query)
        )
    else:
        loas = LOA.objects.all()
    return render(request, 'loa_admin_hr.html', {'loas': loas, 'query': query})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_approver(u))
def loa_submission_overview_admin_hr(request):
    loa_id = request.GET.get('id')
    loa = get_object_or_404(LOA, id=loa_id)
    
    if request.method == 'POST':
        form = LOAAdminForm(request.POST, instance=loa)
        if form.is_valid():
            form.save()
            return redirect('loa_admin_hr')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = LOAAdminForm(instance=loa)
    
    return render(request, 'loa_submission_overview_admin_hr.html', {'form': form, 'loa': loa})

# Creating LOA on behalf of User
@login_required
@user_passes_test(lambda u: is_admin(u) or is_approver(u))
def loa_create_admin_hr(request):
    if request.method == 'POST':
        form = LOAForm(request.POST)
        if form.is_valid():
            loa = form.save(commit=False)
            loa.user = request.user
            loa.save()
            return redirect('loa_admin_hr')
    else:
        form = LOAForm()
    return render(request, 'loa_create_admin_hr.html', {'form': form})

@login_required
@user_passes_test(is_user)
def loa_user(request):
    query = request.GET.get('q', '')
    if query:
        loas = LOA.objects.filter(user=request.user).filter(
            Q(status__icontains(query))
        )
    else:
        loas = LOA.objects.filter(user=request.user)
    return render(request, 'loa_user.html', {'loas': loas, 'query': query})

@login_required
@user_passes_test(is_user)
def loa_submission_overview_user(request):
    loa_id = request.GET.get('id')
    loa = get_object_or_404(LOA, id=loa_id, user=request.user)
    return render(request, 'loa_submission_overview_user.html', {'loa': loa})

@login_required
@user_passes_test(is_user)
def loa_create_user(request):
    if request.method == 'POST':
        form = LOAForm(request.POST)
        if form.is_valid():
            loa = form.save(commit=False)
            loa.user = request.user
            loa.save()
            return redirect('loa_user')
    else:
        form = LOAForm()
    return render(request, 'loa_create_user.html', {'form': form})

@login_required
@user_passes_test(is_user)
def loa_edit_user(request, id):
    loa = get_object_or_404(LOA, id=id, user=request.user)
    if request.method == 'POST':
        form = LOAForm(request.POST, instance=loa)
        if form.is_valid():
            loa.status = 'Pending'
            form.save()
            return redirect('loa_user')
    else:
        form = LOAForm(instance=loa)
    return render(request, 'loa_create_user.html', {'form': form})

@login_required
@user_passes_test(is_user)
def loa_delete_user(request, id):
    loa = get_object_or_404(LOA, id=id, user=request.user)
    loa.delete()
    return redirect('loa_user')

@login_required
@user_passes_test(is_admin)
def settings(request):
    return render(request, 'settings.html')

@login_required
def home_it(request):
    return render(request, 'home_it.html')

@login_required
@user_passes_test(is_it)
def home_it(request):
    return render(request, 'home_it.html')

# Function to dynamically update the `settings.py` with stored credentials
def update_social_auth_backend():
    from django.conf import settings  # Import here to avoid issues with circular imports
    credentials = AzureCredentials.objects.first()
    
    if credentials:
        settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY = credentials.client_id
        settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET = credentials.client_secret
        settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID = credentials.tenant_id

@login_required
@user_passes_test(is_it)
def settings(request):
    if request.method == 'POST':
        form = AzureCredentialsForm(request.POST)
        if form.is_valid():
            AzureCredentials.objects.all().delete()  # Remove existing credentials
            form.save()
            update_social_auth_backend()  # Update the backend with new credentials
            return redirect('home_it')
    else:
        credentials = AzureCredentials.objects.first()
        if credentials:
            form = AzureCredentialsForm(instance=credentials)
        else:
            form = AzureCredentialsForm()
    
    update_social_auth_backend()  # Ensure backend is updated
    return render(request, 'settings.html', {'form': form})