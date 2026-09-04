/**
 * @module routes/onboarding/exit_interview
 * @description Exit interview CRUD routes
 */

from django.urls import path
from core_module.views.api.onboarding.exit_interview import exit_interview_list

urlpatterns = [
    path('', exit_interview_list, name='exit_interview_list'),
]
