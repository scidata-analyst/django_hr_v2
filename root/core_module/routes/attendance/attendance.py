/**
 * @module routes/attendance/attendance
 * @description Attendance module root routes
 */

from django.urls import path, include
from core_module.views.attendance.attendance import attendance

urlpatterns = [
    path('', attendance, name='attendance'),
    path('api/shift/', include('core_module.routes.attendance.shift')),
    path('api/attendance/', include('core_module.routes.attendance.attendance_api')),
    path('api/leave/', include('core_module.routes.attendance.leave')),
]
