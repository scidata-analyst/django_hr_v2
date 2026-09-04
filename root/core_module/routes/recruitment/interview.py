from django.urls import path
from core_module.views.api.recruitment.interview import interview_list, interview_result

urlpatterns = [
    path('', interview_list, name='interview_list'),
    path('<int:pk>/result/', interview_result, name='interview_result'),
]
