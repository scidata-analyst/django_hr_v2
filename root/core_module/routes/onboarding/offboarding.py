from django.urls import path
from core_module.views.api.onboarding.offboarding import offboarding_task_list

urlpatterns = [
    path('', offboarding_task_list, name='offboarding_task_list'),
]
