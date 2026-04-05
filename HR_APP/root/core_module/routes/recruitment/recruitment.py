from django.urls import path
from core_module.views.recruitment.recruitment import recruitment
from core_module.views.api import recruitment_api

urlpatterns = [
    path('', recruitment, name='recruitment'),
    path('api/job/', recruitment_api.job_posting_list, name='job_posting_list'),
    path('api/job/<int:pk>/', recruitment_api.job_posting_detail, name='job_posting_detail'),
    path('api/candidate/', recruitment_api.candidate_list, name='candidate_list'),
    path('api/candidate/<int:pk>/', recruitment_api.candidate_detail, name='candidate_detail'),
    path('api/candidate/<int:pk>/advance/', recruitment_api.candidate_advance, name='candidate_advance'),
    path('api/candidate/<int:pk>/reject/', recruitment_api.candidate_reject, name='candidate_reject'),
    path('api/candidate/pipeline/', recruitment_api.pipeline_summary, name='pipeline_summary'),
    path('api/interview/', recruitment_api.interview_list, name='interview_list'),
    path('api/interview/<int:pk>/result/', recruitment_api.interview_result, name='interview_result'),
]
