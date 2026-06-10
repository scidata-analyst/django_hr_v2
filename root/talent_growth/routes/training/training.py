from django.urls import path
from talent_growth.views.training.training import training
from talent_growth.views.api.training_api import (
    course_list, course_detail,
    enrollment_list, enrollment_complete, enrollment_bulk
)

urlpatterns = [
    path('', training, name='training'),
    path('api/course/', course_list, name='course_list'),
    path('api/course/<int:pk>/', course_detail, name='course_detail'),
    path('api/enrollment/', enrollment_list, name='enrollment_list'),
    path('api/enrollment/<int:pk>/complete/', enrollment_complete, name='enrollment_complete'),
    path('api/enrollment/bulk/', enrollment_bulk, name='enrollment_bulk'),
]
