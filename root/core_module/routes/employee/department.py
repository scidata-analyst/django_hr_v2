from django.urls import path
from core_module.views.api.employee.department import department_list, department_detail

urlpatterns = [
    path('', department_list, name='department_list'),
    path('<int:pk>/', department_detail, name='department_detail'),
]
