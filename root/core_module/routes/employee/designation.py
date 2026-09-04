from django.urls import path
from core_module.views.api import employee_api

urlpatterns = [
    path('', employee_api.designation_list, name='designation_list'),
    path('<int:pk>/', employee_api.designation_detail, name='designation_detail'),
]
