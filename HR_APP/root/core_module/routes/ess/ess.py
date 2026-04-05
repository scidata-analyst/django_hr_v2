from django.urls import path
from core_module.views.ess.ess import ess
from core_module.views.api import ess_api

urlpatterns = [
    path('', ess, name='ess'),
    path('api/expense/', ess_api.expense_claim_list, name='expense_claim_list'),
    path('api/expense/<int:pk>/', ess_api.expense_claim_detail, name='expense_claim_detail'),
    path('api/expense/<int:pk>/approve/', ess_api.expense_claim_approve, name='expense_claim_approve'),
    path('api/expense/<int:pk>/reject/', ess_api.expense_claim_reject, name='expense_claim_reject'),
    path('api/announcement/', ess_api.announcement_list, name='announcement_list'),
]
