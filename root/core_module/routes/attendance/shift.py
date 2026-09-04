from django.urls import path
from core_module.views.api.attendance.shift import shift_list, shift_detail

urlpatterns = [
    path('', shift_list, name='shift_list'),
    path('<int:pk>/', shift_detail, name='shift_detail'),
]
