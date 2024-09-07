from django.urls import path
from . import views

urlpatterns = [
    path('home_admin_hr/', views.home_admin_hr, name='home_admin_hr'),
    path('home_user/', views.home_user, name='home_user'),
    path('onboarding/', views.onboarding, name='onboarding'),
    path('onboarding_submission_overview/', views.onboarding_submission_overview, name='onboarding_submission_overview'),
    path('new_onboarding/', views.new_onboarding, name='new_onboarding'),
    path('edit_onboarding/', views.edit_onboarding, name='edit_onboarding'),
    path('delete_onboarding/', views.delete_onboarding, name='delete_onboarding'),
    path('offboarding/', views.offboarding, name='offboarding'),
    path('offboarding_submission_overview/', views.offboarding_submission_overview, name='offboarding_submission_overview'),
    path('new_offboarding/', views.new_offboarding, name='new_offboarding'),
    path('edit_offboarding/', views.edit_offboarding, name='edit_offboarding'),
    path('delete_offboarding/', views.delete_offboarding, name='delete_offboarding'),
    path('loa_admin_hr/', views.loa_admin_hr, name='loa_admin_hr'),
    path('loa_submission_overview_admin_hr/', views.loa_submission_overview_admin_hr, name='loa_submission_overview_admin_hr'),
    path('loa_create/', views.loa_create, name='loa_create'), # This line is crucial
    path('loa_user/', views.loa_user, name='loa_user'),
    path('loa_submission_overview_user/', views.loa_submission_overview_user, name='loa_submission_overview_user'),
    path('loa_edit_user/<int:id>/', views.loa_edit_user, name='loa_edit_user'),
    path('loa_delete_user/<int:id>/', views.loa_delete_user, name='loa_delete_user'),
    path('settings/', views.settings, name='settings'),
    path('configuration/', views.configuration, name='configuration'),
    path('home_it/', views.home_it, name='home_it'),
    path('backup_now/', views.backup_now, name='backup_now'),
    path('restore_from_backup/', views.restore_from_backup, name='restore_from_backup'),
]