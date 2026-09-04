/**
 * @module routes/onboarding/onboarding_task
 * @description Onboarding task CRUD routes
 */

from django.urls import path
from core_module.views.api.onboarding.onboarding_task import onboarding_task_list, onboarding_task_detail

urlpatterns = [
    path('', onboarding_task_list, name='onboarding_task_list'),
    path('<int:pk>/', onboarding_task_detail, name='onboarding_task_detail'),
]
