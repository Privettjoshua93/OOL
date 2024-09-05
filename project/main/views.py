from .models import AzureCredentials
from .forms import AzureCredentialsForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Onboarding, Offboarding, LOA
from .forms import OnboardingForm, OffboardingForm, LOAForm, LOAAdminForm, OffboardingAdminForm, OnboardingAdminForm
import json
from django.contrib.auth.models import Group, User 
from social_django.utils import load_strategy
from .models import AzureCredentials
from .forms import AzureCredentialsForm
from django.urls import reverse
from .utils import get_user_emails_by_group, send_email
import requests

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
@user_passes_test(lambda u: is_admin(u) or is_it(u))
def home_admin_hr(request):
    if is_it(request.user):
        return redirect('home_it')
    if not is_admin(request.user):
        return redirect(['home_user'])
    return render(request, 'home_admin_hr.html')

@login_required
def home_user(request):
    if is_approver(request.user):
        return redirect('loa_admin_hr')
    return render(request, 'home_user.html')

@login_required
def home_it(request):
    if not is_it(request.user):  # Prevent unauthorized access to IT home
        return redirect('login_redirect')
    return render(request, 'home_it.html')

@login_required
@user_passes_test(lambda user: is_admin(user) or is_it(user))
def onboarding(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', 'start_date_desc')
    status_filter = request.GET.get('status_filter', 'pending')

    # Set the initial queryset
    onboardings = Onboarding.objects.all()

    # Apply search filter if query is provided
    if query:
        onboardings = onboardings.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(status__icontains=query)
        )

    # Apply status filter
    if status_filter == 'pending':
        onboardings = onboardings.filter(status='Pending')
    elif status_filter == 'complete':
        onboardings = onboardings.filter(status='Complete')

    # Apply sorting
    if sort_by == 'start_date_asc':
        onboardings = onboardings.order_by('start_date')
    elif sort_by == 'start_date_desc':
        onboardings = onboardings.order_by('-start_date')

    return render(request, 'onboarding.html', {'onboardings': onboardings, 'query': query, 'sort_by': sort_by, 'status_filter': status_filter})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_it(u))
def onboarding_submission_overview(request):
    onboarding_id = request.GET.get('id')
    onboarding = get_object_or_404(Onboarding, id=onboarding_id)
    if request.method == 'POST':
        form = OnboardingAdminForm(request.POST, instance=onboarding)
        if form.is_valid():
            form.save()
            recipient_list = get_user_emails_by_group('Admin') + get_user_emails_by_group('IT')
            details_dict = {
                'First Name': onboarding.first_name,
                'Last Name': onboarding.last_name,
                'Preferred Work Email': onboarding.preferred_work_email,
                'Personal Email': onboarding.personal_email,
                'Mobile Number': onboarding.mobile_number,
                'Title': onboarding.title,
                'Manager': onboarding.manager,
                'Department': onboarding.department,
                'Mac or PC': onboarding.mac_or_pc,
                'Start Date': onboarding.start_date,
                'Location': onboarding.location,
                'Groups': onboarding.groups,
                'Distribution Lists': onboarding.distribution_lists,
                'Shared Drives': onboarding.shared_drives,
                'Status': onboarding.status,
            }
            send_email(
                'Onboarding Status Updated',
                details_dict,
                recipient_list
            )
            return redirect('onboarding')
    else:
        form = OnboardingAdminForm(instance=onboarding)
    return render(request, 'onboarding_submission_overview.html', {'form': form, 'onboarding': onboarding})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_it(u))
def new_onboarding(request):
    if request.method == 'POST':
        form = OnboardingForm(request.POST)
        if form.is_valid():
            onboarding = form.save()
            recipient_list = get_user_emails_by_group('Admin') + get_user_emails_by_group('IT')
            details_dict = {
                'First Name': onboarding.first_name,
                'Last Name': onboarding.last_name,
                'Preferred Work Email': onboarding.preferred_work_email,
                'Personal Email': onboarding.personal_email,
                'Mobile Number': onboarding.mobile_number,
                'Title': onboarding.title,
                'Manager': onboarding.manager,
                'Department': onboarding.department,
                'Mac or PC': onboarding.mac_or_pc,
                'Start Date': onboarding.start_date,
                'Location': onboarding.location,
                'Groups': onboarding.groups,
                'Distribution Lists': onboarding.distribution_lists,
                'Shared Drives': onboarding.shared_drives,
                'Status': onboarding.status,
            }
            send_email(
                'New Onboarding Created',
                details_dict,
                recipient_list
            )
            return redirect('onboarding')
    else:
        form = OnboardingForm()
    return render(request, 'new_onboarding.html', {'form': form})

@login_required
@user_passes_test(lambda user: is_admin(user) or is_it(user))
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
@user_passes_test(lambda user: is_admin(user) or is_it(user))
def delete_onboarding(request):
    onboarding_id = request.GET.get('id')
    onboarding = get_object_or_404(Onboarding, id=onboarding_id)
    onboarding.delete()
    return redirect('onboarding')

@login_required
@user_passes_test(lambda user: is_admin(user) or is_it(user))
def offboarding(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', 'last_date_time_desc')
    status_filter = request.GET.get('status_filter', 'pending')

    # Set the initial queryset
    offboardings = Offboarding.objects.all()

    # Apply search filter if query is provided
    if query:
        offboardings = offboardings.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(status__icontains=query)
        )

    # Apply status filter
    if status_filter == 'pending':
        offboardings = offboardings.filter(status='Pending')
    elif status_filter == 'complete':
        offboardings = offboardings.filter(status='Complete')

    # Apply sorting
    if sort_by == 'last_date_time_asc':
        offboardings = offboardings.order_by('last_date_time')
    elif sort_by == 'last_date_time_desc':
        offboardings = offboardings.order_by('-last_date_time')

    return render(request, 'offboarding.html', {'offboardings': offboardings, 'query': query, 'sort_by': sort_by, 'status_filter': status_filter})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_it(u))
def offboarding_submission_overview(request):
    offboarding_id = request.GET.get('id')
    offboarding = get_object_or_404(Offboarding, id=offboarding_id)
    if request.method == 'POST':
        form = OffboardingAdminForm(request.POST, instance=offboarding)
        if form.is_valid():
            form.save()
            recipient_list = get_user_emails_by_group('Admin') + get_user_emails_by_group('IT')
            details_dict = {
                'First Name': offboarding.first_name,
                'Last Name': offboarding.last_name,
                'Last Date/Time': offboarding.last_date_time,
                'Additional Notes': offboarding.additional_notes,
                'Status': offboarding.status,
            }
            send_email(
                'Offboarding Status Updated',
                details_dict,
                recipient_list
            )
            return redirect('offboarding')
    else:
        form = OffboardingAdminForm(instance=offboarding)
    return render(request, 'offboarding_submission_overview.html', {'form': form})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_it(u))
def new_offboarding(request):
    if request.method == 'POST':
        form = OffboardingForm(request.POST)
        if form.is_valid():
            offboarding = form.save()
            recipient_list = get_user_emails_by_group('Admin') + get_user_emails_by_group('IT')
            details_dict = {
                'First Name': offboarding.first_name,
                'Last Name': offboarding.last_name,
                'Last Date/Time': offboarding.last_date_time,
                'Additional Notes': offboarding.additional_notes,
                'Status': offboarding.status,
            }
            send_email(
                'New Offboarding Created',
                details_dict,
                recipient_list
            )
            return redirect('offboarding')
    else:
        form = OffboardingForm()
    return render(request, 'new_offboarding.html', {'form': form})

@login_required
@user_passes_test(lambda user: is_admin(user) or is_it(user))
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
@user_passes_test(lambda user: is_admin(user) or is_it(user))
def delete_offboarding(request):
    offboarding_id = request.GET.get('id')
    offboarding = get_object_or_404(Offboarding, id=offboarding_id)
    offboarding.delete()
    return redirect('offboarding')

# LOA Admin Overview View
@login_required
@user_passes_test(lambda user: is_admin(user) or is_approver(user) or is_it(user))
def loa_admin_hr(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', 'start_date_desc')
    status_filter = request.GET.get('status_filter', 'pending')

    # Set the initial queryset
    loas = LOA.objects.all()

    # Apply search filter if query is provided
    if query:
        loas = loas.filter(
            Q(user__username__icontains=query) | Q(status__icontains=query)
        )

    # Apply status filter
    if status_filter == 'pending':
        loas = loas.filter(status='Pending')
    elif status_filter == 'approved':
        loas = loas.filter(status='Approved')
    elif status_filter == 'denied':
        loas = loas.filter(status='Denied')

    # Apply sorting
    if sort_by == 'start_date_asc':
        loas = loas.order_by('start_date')
    elif sort_by == 'start_date_desc':
        loas = loas.order_by('-start_date')
    elif sort_by == 'last_date_asc':
        loas = loas.order_by('last_date')
    elif sort_by == 'last_date_desc':
        loas = loas.order_by('-last_date')

    return render(request, 'loa_admin_hr.html', {'loas': loas, 'query': query, 'sort_by': sort_by, 'status_filter': status_filter})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_approver(u) or is_it(u))
def loa_submission_overview_admin_hr(request):
    loa_id = request.GET.get('id')
    loa = get_object_or_404(LOA, id=loa_id)
    if request.method == 'POST':
        form = LOAAdminForm(request.POST, instance=loa)
        if form.is_valid():
            form.save()
            # Notify both the user and approvers
            approver_emails = get_user_emails_by_group('Approver')
            recipient_list = approver_emails + [loa.user.email]  # Both approver and submitter
            details_dict = {
                'First Name': loa.user.first_name,
                'Last Name': loa.user.last_name,
                'Start Date': loa.start_date,
                'End Date': loa.end_date,
                'Status': loa.status,
            }
            send_email(
                'LOA Status Updated',
                details_dict,
                recipient_list
            )
            return redirect('loa_admin_hr')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = LOAAdminForm(instance=loa)
    return render(request, 'loa_submission_overview_admin_hr.html', {'form': form, 'loa': loa})

import logging

# Set up logging
logger = logging.getLogger(__name__)

@login_required
@user_passes_test(lambda u: is_admin(u) or is_approver(u) or is_it(u))
def loa_create_admin_hr(request):
    if request.method == 'POST':
        form = LOAForm(request.POST)
        if form.is_valid():
            loa = form.save(commit=False)
            loa.user = request.user
            loa.save()
            # Notify approver users via email
            approver_emails = get_user_emails_by_group('Approver')
            recipient_list = approver_emails + [loa.user.email]  # Both approver and submitter
            details_dict = {
                'First Name': loa.user.first_name,
                'Last Name': loa.user.last_name,
                'Start Date': loa.start_date,
                'End Date': loa.end_date,
                'Status': loa.status,
            }
            send_email(
                'New LOA Created',
                details_dict,
                recipient_list
            )
            return redirect('loa_admin_hr')
    else:
        form = LOAForm()
    return render(request, 'loa_create_admin_hr.html', {'form': form})

@login_required
@user_passes_test(is_user)
def loa_user(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', 'start_date_desc')
    status_filter = request.GET.get('status_filter', 'pending')

    # Set the initial queryset
    loas = LOA.objects.filter(user=request.user)

    # Apply search filter if query is provided
    if query:
        loas = loas.filter(
            Q(status__icontains=query)
        )

    # Apply status filter
    if status_filter == 'pending':
        loas = loas.filter(status='Pending')
    elif status_filter == 'approved':
        loas = loas.filter(status='Approved')
    elif status_filter == 'denied':
        loas = loas.filter(status='Denied')

    # Apply sorting
    if sort_by == 'start_date_asc':
        loas = loas.order_by('start_date')
    elif sort_by == 'start_date_desc':
        loas = loas.order_by('-start_date')
    elif sort_by == 'last_date_asc':
        loas = loas.order_by('last_date')
    elif sort_by == 'last_date_desc':
        loas = loas.order_by('-last_date')

    return render(request, 'loa_user.html', {'loas': loas, 'query': query, 'sort_by': sort_by, 'status_filter': status_filter})

@login_required
@user_passes_test(is_user)
def loa_submission_overview_user(request):
    loa_id = request.GET.get('id')
    loa = get_object_or_404(LOA, id=loa_id, user=request.user)
    return render(request, 'loa_submission_overview_user.html', {'loa': loa})

@login_required
@user_passes_test(lambda u: is_user(u) or is_admin(u) or is_approver(u) or is_it(u))
def loa_create_user(request):
    if request.method == 'POST':
        form = LOAForm(request.POST)
        if form.is_valid():
            loa = form.save(commit=False)
            loa.user = request.user
            loa.save()
            # Notify both the user and approvers
            approver_emails = get_user_emails_by_group('Approver')
            recipient_list = approver_emails + [loa.user.email]  # Both approver and submitter
            details_dict = {
                'First Name': loa.user.first_name,
                'Last Name': loa.user.last_name,
                'Start Date': loa.start_date,
                'End Date': loa.end_date,
                'Status': loa.status,
            }
            send_email(
                'New LOA Created',
                details_dict,
                recipient_list
            )
            if is_admin(request.user) or is_approver(request.user) or is_it(request.user):
                return redirect('loa_admin_hr')
            else:
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
            recipient_list = get_user_emails_by_group('Approver')
            send_email(
                'LOA Status Changed to Pending',
                'A leave of absence entry has been edited and marked as pending.',
                recipient_list
            )
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

        # Update SMTP settings
        settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        settings.EMAIL_HOST = credentials.smtp_host
        settings.EMAIL_PORT = credentials.smtp_port
        settings.EMAIL_HOST_USER = credentials.smtp_user
        settings.EMAIL_HOST_PASSWORD = credentials.smtp_password  # Decryption handled by EncryptedCharField
        settings.DEFAULT_FROM_EMAIL = credentials.smtp_user  # Optional, if you want to set the default from email

        # Ensure TLS or SSL is set correctly
        settings.EMAIL_USE_TLS = True
        settings.EMAIL_USE_SSL = False
        
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

    # Ensure backend is updated before render ensuring decrypt email configurations
    update_social_auth_backend()
    return render(request, 'settings.html', {'form': form})

@login_required
def login_redirect(request):
    if is_it(request.user):
        group = Group.objects.get(name='IT')
        request.user.groups.add(group)
        return redirect('home_it')
    elif is_admin(request.user):
        group = Group.objects.get(name='Admin')
        request.user.groups.add(group)
        return redirect('home_admin_hr')
    elif is_approver(request.user):
        group = Group.objects.get(name='Approver')
        request.user.groups.add(group)
        return redirect('loa_admin_hr')
    else:
        group = Group.objects.get(name='User')
        request.user.groups.add(group)
        return redirect('home_user')
    

# Custom save user in pipeline step
def custom_save_user_in_pipeline(backend, user=None, response=None, *args, **kwargs):
    if backend.name == 'azuread-tenant-oauth2' and user:
        strategy = load_strategy()

        # Extract additional user details from the response
        first_name = response.get('givenName', 'Unknown')
        last_name = response.get('surname', 'User')

        # Update user details
        user.first_name = first_name
        user.last_name = last_name

        # Fetch the access token from the strategy's session
        access_token = strategy.session_get('access_token')
        headers = {'Authorization': f'Bearer {access_token}'}
        groups_url = 'https://graph.microsoft.com/v1.0/me/memberOf'

        # Make the API request to fetch user groups
        groups_response = requests.get(groups_url, headers=headers)
        if groups_response.status_code == 200:
            groups_data = groups_response.json()

            # Clear current groups and reassign based on Azure AD
            user.groups.clear()

            for group in groups_data.get("value", []):
                group_name = group.get("displayName")
                if group_name:
                    # Ensure the group exists
                    group, created = Group.objects.get_or_create(name=group_name)
                    user.groups.add(group)

        user.save()

LOGIN_REDIRECT_URL = '/login_redirect/'



settings.SOCIAL_AUTH_AZUREAD_TENANT_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',  # Ensure association by email
    'social_core.pipeline.user.create_user',
    'main.views.custom_save_user_in_pipeline',  # Custom pipeline step
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)