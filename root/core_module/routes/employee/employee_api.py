from django.urls import path
from core_module.views.api import employee_api

urlpatterns = [
    path('', employee_api.employee_list, name='employee_list'),
    path('<int:pk>/', employee_api.employee_detail_api, name='employee_detail_api'),
    path('stats/', employee_api.employee_stats, name='employee_stats'),
]
