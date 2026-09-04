from django.urls import path
from core_module.views.api import payroll_api

urlpatterns = [
    path('', payroll_api.salary_structure_list, name='salary_structure_list'),
    path('<int:pk>/', payroll_api.salary_structure_detail, name='salary_structure_detail'),
]
