from django.urls import path
from core_module.views.api import employee_api

urlpatterns = [
    path('', employee_api.department_list, name='department_list'),
    path('<int:pk>/', employee_api.department_detail, name='department_detail'),
]
