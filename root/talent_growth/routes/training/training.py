from django.urls import path
from talent_growth.views.training.training import training
from talent_growth.views.api import talent_api

urlpatterns = [
    path('', training, name='training'),
    path('api/course/', talent_api.course_list, name='course_list'),
    path('api/course/<int:pk>/', talent_api.course_detail, name='course_detail'),
    path('api/enrollment/', talent_api.enrollment_list, name='enrollment_list'),
    path('api/enrollment/<int:pk>/complete/', talent_api.enrollment_complete, name='enrollment_complete'),
    path('api/enrollment/bulk/', talent_api.enrollment_bulk, name='enrollment_bulk'),
]
