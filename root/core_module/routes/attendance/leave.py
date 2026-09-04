/**
 * @module routes/attendance/leave
 * @description Leave request CRUD and action routes
 */

from django.urls import path
from core_module.views.api.attendance.leave import leave_list, leave_detail, leave_approve, leave_deny

urlpatterns = [
    path('', leave_list, name='leave_list'),
    path('<int:pk>/', leave_detail, name='leave_detail'),
    path('<int:pk>/approve/', leave_approve, name='leave_approve'),
    path('<int:pk>/deny/', leave_deny, name='leave_deny'),
]
