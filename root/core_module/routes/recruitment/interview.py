from django.urls import path
from core_module.views.api import recruitment_api

urlpatterns = [
    path('', recruitment_api.interview_list, name='interview_list'),
    path('<int:pk>/result/', recruitment_api.interview_result, name='interview_result'),
]
