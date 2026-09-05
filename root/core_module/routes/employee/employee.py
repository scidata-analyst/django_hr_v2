"""
@module routes/employee/employee
@description Employee CRUD and stats routes
"""

from django.urls import path
from core_module.views.api.employee.employee import employee_list, employee_detail_api, employee_stats

urlpatterns = [
    path('', employee_list, name='employee_list'),
    path('<int:pk>/', employee_detail_api, name='employee_detail_api'),
    path('stats/', employee_stats, name='employee_stats'),
]
