from django.urls import path
from core_module.views.api import onboarding_api

urlpatterns = [
    path('', onboarding_api.exit_interview_list, name='exit_interview_list'),
]
