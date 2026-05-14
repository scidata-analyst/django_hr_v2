from django.urls import path
from core_module.views.attendance.attendance import attendance
from core_module.views.api import attendance_api

urlpatterns = [
    path('', attendance, name='attendance'),
    path('api/shift/', attendance_api.shift_list, name='shift_list'),
    path('api/shift/<int:pk>/', attendance_api.shift_detail, name='shift_detail'),
    path('api/attendance/', attendance_api.attendance_list, name='attendance_list'),
    path('api/attendance/<int:pk>/', attendance_api.attendance_detail, name='attendance_detail'),
    path('api/attendance/stats/', attendance_api.attendance_stats, name='attendance_stats'),
    path('api/attendance/<int:employee_id>/stats/', attendance_api.employee_attendance_stats, name='employee_attendance_stats'),
    path('api/leave/', attendance_api.leave_list, name='leave_list'),
    path('api/leave/<int:pk>/', attendance_api.leave_detail, name='leave_detail'),
    path('api/leave/<int:pk>/approve/', attendance_api.leave_approve, name='leave_approve'),
    path('api/leave/<int:pk>/deny/', attendance_api.leave_deny, name='leave_deny'),
]
