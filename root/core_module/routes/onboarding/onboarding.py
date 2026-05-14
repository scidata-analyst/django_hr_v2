from django.urls import path
from core_module.views.onboarding.onboarding import onboarding
from core_module.views.api import onboarding_api

urlpatterns = [
    path('', onboarding, name='onboarding'),
    path('api/task/', onboarding_api.onboarding_task_list, name='onboarding_task_list'),
    path('api/task/<int:pk>/', onboarding_api.onboarding_task_detail, name='onboarding_task_detail'),
    path('api/offboarding/', onboarding_api.offboarding_task_list, name='offboarding_task_list'),
    path('api/exit-interview/', onboarding_api.exit_interview_list, name='exit_interview_list'),
]
