from django.shortcuts import render

def home_admin_hr(request):
    return render(request, 'home_admin_hr.html')

def home_user(request):
    return render(request, 'home_user.html')

def onboarding(request):
    return render(request, 'onboarding.html')

def onboarding_submission_overview(request):
    return render(request, 'onboarding_submission_overview.html')

def new_onboarding(request):
    return render(request, 'new_onboarding.html')

def offboarding(request):
    return render(request, 'offboarding.html')

def offboarding_submission_overview(request):
    return render(request, 'offboarding_submission_overview.html')

def new_offboarding(request):
    return render(request, 'new_offboarding.html')

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