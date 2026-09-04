from django.urls import path
from core_module.views.api import recruitment_api

urlpatterns = [
    path('job/', recruitment_api.job_posting_list, name='job_posting_list'),
    path('job/<int:pk>/', recruitment_api.job_posting_detail, name='job_posting_detail'),
]
