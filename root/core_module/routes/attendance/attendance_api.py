from django.urls import path
from core_module.views.api.attendance.attendance_api import attendance_list, attendance_detail, attendance_stats, employee_attendance_stats

urlpatterns = [
    path('', attendance_list, name='attendance_list'),
    path('<int:pk>/', attendance_detail, name='attendance_detail'),
    path('stats/', attendance_stats, name='attendance_stats'),
    path('<int:employee_id>/stats/', employee_attendance_stats, name='employee_attendance_stats'),
]
