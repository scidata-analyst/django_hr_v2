from django.urls import path
from core_module.views.api import recruitment_api

urlpatterns = [
    path('', recruitment_api.candidate_list, name='candidate_list'),
    path('<int:pk>/', recruitment_api.candidate_detail, name='candidate_detail'),
    path('<int:pk>/advance/', recruitment_api.candidate_advance, name='candidate_advance'),
    path('<int:pk>/reject/', recruitment_api.candidate_reject, name='candidate_reject'),
    path('pipeline/', recruitment_api.pipeline_summary, name='pipeline_summary'),
]
