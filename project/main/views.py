from django.shortcuts import render, redirect, get_object_or_404
from .models import Onboarding, Offboarding
from .forms import OnboardingForm, OffboardingForm
from django.db.models import Q

def home_admin_hr(request):
    return render(request, 'home_admin_hr.html')

def home_user(request):
    return render(request, 'home_user.html')

def onboarding(request):
    query = request.GET.get('q', '')
    if query:
        onboardings = Onboarding.objects.filter(
            Q(employee_name__icontains=query) |
            Q(status__icontains=query) |
            Q(details__icontains=query)
        )
    else:
        onboardings = Onboarding.objects.all()
    return render(request, 'onboarding.html', {'onboardings': onboardings, 'query': query})

def onboarding_submission_overview(request):
    onboarding_id = request.GET.get('id')
    onboarding = get_object_or_404(Onboarding, id=onboarding_id)
    return render(request, 'onboarding_submission_overview.html', {'onboarding': onboarding})

def new_onboarding(request):
    if request.method == 'POST':
        form = OnboardingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('onboarding')
    else:
        form = OnboardingForm()
    return render(request, 'new_onboarding.html', {'form': form})

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

def delete_onboarding(request):
    onboarding_id = request.GET.get('id')
    onboarding = get_object_or_404(Onboarding, id=onboarding_id)
    onboarding.delete()
    return redirect('onboarding')

def offboarding(request):
    query = request.GET.get('q', '')
    if query:
        offboardings = Offboarding.objects.filter(
            Q(employee_name__icontains=query) |
            Q(status__icontains=query) |
            Q(details__icontains=query)
        )
    else:
        offboardings = Offboarding.objects.all()
    return render(request, 'offboarding.html', {'offboardings': offboardings, 'query': query})

def offboarding_submission_overview(request):
    offboarding_id = request.GET.get('id')
    offboarding = get_object_or_404(Offboarding, id=offboarding_id)
    return render(request, 'offboarding_submission_overview.html', {'offboarding': offboarding})

def new_offboarding(request):
    if request.method == 'POST':
        form = OffboardingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('offboarding')
    else:
        form = OffboardingForm()
    return render(request, 'new_offboarding.html', {'form': form})

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

def delete_offboarding(request):
    offboarding_id = request.GET.get('id')
    offboarding = get_object_or_404(Offboarding, id=offboarding_id)
    offboarding.delete()
    return redirect('offboarding')

def loa_admin_hr(request):
    return render(request, 'loa_admin_hr.html')

def loa_submission_overview_admin_hr(request):
    return render(request, 'loa_submission_overview_admin_hr.html')

def loa_create_admin_hr(request):
    return render(request, 'loa_create_admin_hr.html')

def loa_user(request):
    return render(request, 'loa_user.html')

def loa_submission_overview_user(request):
    return render(request, 'loa_submission_overview_user.html')

def loa_create_user(request):
    return render(request, 'loa_create_user.html')

def settings(request):
    return render(request, 'settings.html')