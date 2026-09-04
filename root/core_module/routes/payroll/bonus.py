from django.urls import path
from core_module.views.api import payroll_api

urlpatterns = [
    path('', payroll_api.bonus_list, name='bonus_list'),
]
