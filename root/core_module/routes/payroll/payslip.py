from django.urls import path
from core_module.views.api import payroll_api

urlpatterns = [
    path('', payroll_api.payslip_list, name='payslip_list'),
    path('<int:pk>/', payroll_api.payslip_detail, name='payslip_detail'),
    path('bulk-generate/', payroll_api.payslip_bulk_generate, name='payslip_bulk_generate'),
]
