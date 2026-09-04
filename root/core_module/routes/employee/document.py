from django.urls import path
from core_module.views.api import employee_api

urlpatterns = [
    path('', employee_api.document_list, name='document_list'),
]
