"""
@module routes/payroll/bonus
@description Bonus CRUD routes
"""

from django.urls import path
from core_module.views.api.payroll.bonus import bonus_list, bonus_detail

urlpatterns = [
    path('', bonus_list, name='bonus_list'),
    path('<int:pk>/', bonus_detail, name='bonus_detail'),
]
