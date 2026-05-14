from django.urls import path
from core_module.views.payroll.payroll import payroll
from core_module.views.api import payroll_api

urlpatterns = [
    path('', payroll, name='payroll'),
    path('api/structure/', payroll_api.salary_structure_list, name='salary_structure_list'),
    path('api/structure/<int:pk>/', payroll_api.salary_structure_detail, name='salary_structure_detail'),
    path('api/payslip/', payroll_api.payslip_list, name='payslip_list'),
    path('api/payslip/<int:pk>/', payroll_api.payslip_detail, name='payslip_detail'),
    path('api/payslip/bulk-generate/', payroll_api.payslip_bulk_generate, name='payslip_bulk_generate'),
    path('api/loan/', payroll_api.loan_list, name='loan_list'),
    path('api/loan/<int:pk>/', payroll_api.loan_detail, name='loan_detail'),
    path('api/loan/<int:pk>/approve/', payroll_api.loan_approve, name='loan_approve'),
    path('api/bonus/', payroll_api.bonus_list, name='bonus_list'),
]
