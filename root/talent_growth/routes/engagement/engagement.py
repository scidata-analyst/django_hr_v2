from django.urls import path
from talent_growth.views.engagement.engagement import engagement
from talent_growth.views.api.engagement_api import (
    survey_list, recognition_list, employee_points
)

urlpatterns = [
    path('', engagement, name='engagement'),
    path('api/survey/', survey_list, name='survey_list'),
    path('api/recognition/', recognition_list, name='recognition_list'),
    path('api/recognition/<int:employee_id>/points/', employee_points, name='employee_points'),
]
