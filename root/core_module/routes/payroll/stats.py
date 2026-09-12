"""
@module routes/payroll/stats
@description Payroll aggregated stats routes
"""

from django.urls import path
from core_module.views.api.payroll.payslip import payroll_stats, payroll_breakdown

urlpatterns = [
    path('', payroll_stats, name='payroll_stats'),
    path('breakdown/', payroll_breakdown, name='payroll_breakdown'),
]
