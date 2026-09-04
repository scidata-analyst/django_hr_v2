from django.urls import path
from core_module.views.api import attendance_api

urlpatterns = [
    path('', attendance_api.leave_list, name='leave_list'),
    path('<int:pk>/', attendance_api.leave_detail, name='leave_detail'),
    path('<int:pk>/approve/', attendance_api.leave_approve, name='leave_approve'),
    path('<int:pk>/deny/', attendance_api.leave_deny, name='leave_deny'),
]
