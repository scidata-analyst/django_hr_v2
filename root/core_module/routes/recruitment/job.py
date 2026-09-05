"""
@module routes/recruitment/job
@description Job posting CRUD routes
"""

from django.urls import path
from core_module.views.api.recruitment.job import job_posting_list, job_posting_detail

urlpatterns = [
    path('', job_posting_list, name='job_posting_list'),
    path('<int:pk>/', job_posting_detail, name='job_posting_detail'),
]
