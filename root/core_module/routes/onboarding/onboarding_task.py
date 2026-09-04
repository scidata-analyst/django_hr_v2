from django.urls import path
from core_module.views.api import onboarding_api

urlpatterns = [
    path('', onboarding_api.onboarding_task_list, name='onboarding_task_list'),
    path('<int:pk>/', onboarding_api.onboarding_task_detail, name='onboarding_task_detail'),
]
