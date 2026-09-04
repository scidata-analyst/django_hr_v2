from django.urls import path
from core_module.views.api import onboarding_api

urlpatterns = [
    path('', onboarding_api.offboarding_task_list, name='offboarding_task_list'),
]
