from django.urls import path
from core_module.views.api import ess_api

urlpatterns = [
    path('', ess_api.expense_claim_list, name='expense_claim_list'),
    path('<int:pk>/', ess_api.expense_claim_detail, name='expense_claim_detail'),
    path('<int:pk>/approve/', ess_api.expense_claim_approve, name='expense_claim_approve'),
    path('<int:pk>/reject/', ess_api.expense_claim_reject, name='expense_claim_reject'),
]
