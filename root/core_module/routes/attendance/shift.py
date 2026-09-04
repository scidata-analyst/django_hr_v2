from django.urls import path
from core_module.views.api import attendance_api

urlpatterns = [
    path('', attendance_api.shift_list, name='shift_list'),
    path('<int:pk>/', attendance_api.shift_detail, name='shift_detail'),
]
