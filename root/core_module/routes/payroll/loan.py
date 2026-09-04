/**
 * @module routes/payroll/loan
 * @description Loan CRUD and approval routes
 */

from django.urls import path
from core_module.views.api.payroll.loan import loan_list, loan_detail, loan_approve

urlpatterns = [
    path('', loan_list, name='loan_list'),
    path('<int:pk>/', loan_detail, name='loan_detail'),
    path('<int:pk>/approve/', loan_approve, name='loan_approve'),
]
