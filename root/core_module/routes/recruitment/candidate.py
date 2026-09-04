"""
@module routes/recruitment/candidate
@description Candidate CRUD and pipeline routes
"""

from django.urls import path
from core_module.views.api.recruitment.candidate import candidate_list, candidate_detail, candidate_advance, candidate_reject, pipeline_summary

urlpatterns = [
    path('', candidate_list, name='candidate_list'),
    path('<int:pk>/', candidate_detail, name='candidate_detail'),
    path('<int:pk>/advance/', candidate_advance, name='candidate_advance'),
    path('<int:pk>/reject/', candidate_reject, name='candidate_reject'),
    path('pipeline/', pipeline_summary, name='pipeline_summary'),
]
