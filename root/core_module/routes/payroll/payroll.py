from django.urls import path, include
from core_module.views.payroll.payroll import payroll

urlpatterns = [
    path('', payroll, name='payroll'),
    path('api/structure/', include('core_module.routes.payroll.structure')),
    path('api/payslip/', include('core_module.routes.payroll.payslip')),
    path('api/loan/', include('core_module.routes.payroll.loan')),
    path('api/bonus/', include('core_module.routes.payroll.bonus')),
]
