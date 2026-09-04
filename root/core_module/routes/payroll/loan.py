from django.urls import path
from core_module.views.api import payroll_api

urlpatterns = [
    path('', payroll_api.loan_list, name='loan_list'),
    path('<int:pk>/', payroll_api.loan_detail, name='loan_detail'),
    path('<int:pk>/approve/', payroll_api.loan_approve, name='loan_approve'),
]
