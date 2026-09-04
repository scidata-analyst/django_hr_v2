/**
 * @module routes/employee/document
 * @description Document CRUD routes
 */

from django.urls import path
from core_module.views.api.employee.document import document_list

urlpatterns = [
    path('', document_list, name='document_list'),
]
