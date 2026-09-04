from django.urls import path
from core_module.views.api.payroll.payslip import payslip_list, payslip_detail, payslip_bulk_generate

urlpatterns = [
    path('', payslip_list, name='payslip_list'),
    path('<int:pk>/', payslip_detail, name='payslip_detail'),
    path('bulk-generate/', payslip_bulk_generate, name='payslip_bulk_generate'),
]
