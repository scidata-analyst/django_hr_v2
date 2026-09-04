from django.urls import path
from core_module.views.api.employee.designation import designation_list, designation_detail

urlpatterns = [
    path('', designation_list, name='designation_list'),
    path('<int:pk>/', designation_detail, name='designation_detail'),
]
