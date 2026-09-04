from django.urls import path
from core_module.views.api import attendance_api

urlpatterns = [
    path('', attendance_api.attendance_list, name='attendance_list'),
    path('<int:pk>/', attendance_api.attendance_detail, name='attendance_detail'),
    path('stats/', attendance_api.attendance_stats, name='attendance_stats'),
    path('<int:employee_id>/stats/', attendance_api.employee_attendance_stats, name='employee_attendance_stats'),
]
