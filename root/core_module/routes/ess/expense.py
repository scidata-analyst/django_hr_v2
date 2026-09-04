"""
@module routes/ess/expense
@description Expense claim CRUD and action routes
"""

from django.urls import path
from core_module.views.api.ess.expense import expense_claim_list, expense_claim_detail, expense_claim_approve, expense_claim_reject

urlpatterns = [
    path('', expense_claim_list, name='expense_claim_list'),
    path('<int:pk>/', expense_claim_detail, name='expense_claim_detail'),
    path('<int:pk>/approve/', expense_claim_approve, name='expense_claim_approve'),
    path('<int:pk>/reject/', expense_claim_reject, name='expense_claim_reject'),
]
