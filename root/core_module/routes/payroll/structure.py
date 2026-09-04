from django.urls import path
from core_module.views.api.payroll.structure import salary_structure_list, salary_structure_detail

urlpatterns = [
    path('', salary_structure_list, name='salary_structure_list'),
    path('<int:pk>/', salary_structure_detail, name='salary_structure_detail'),
]
