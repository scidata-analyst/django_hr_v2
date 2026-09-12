"""
@module routes/attendance/leave
@description Leave request CRUD and action routes
"""

from django.urls import path
from core_module.views.api.attendance.leave import leave_list, leave_detail, leave_approve, leave_deny, leave_balance_stats

urlpatterns = [
    path('stats/', leave_balance_stats, name='leave_balance_stats'),
    path('', leave_list, name='leave_list'),
    path('<int:pk>/', leave_detail, name='leave_detail'),
    path('<int:pk>/approve/', leave_approve, name='leave_approve'),
    path('<int:pk>/deny/', leave_deny, name='leave_deny'),
]
