from django.urls import path
from talent_growth.views.engagement.engagement import engagement
from talent_growth.views.api import talent_api

urlpatterns = [
    path('', engagement, name='engagement'),
    path('api/survey/', talent_api.survey_list, name='survey_list'),
    path('api/recognition/', talent_api.recognition_list, name='recognition_list'),
    path('api/recognition/<int:employee_id>/points/', talent_api.employee_points, name='employee_points'),
]
