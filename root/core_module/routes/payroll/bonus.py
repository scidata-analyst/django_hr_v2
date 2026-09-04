from django.urls import path
from core_module.views.api.payroll.bonus import bonus_list

urlpatterns = [
    path('', bonus_list, name='bonus_list'),
]
