/**
 * @module routes/employee/location
 * @description Location CRUD routes
 */

from django.urls import path
from core_module.views.api.employee.location import location_list, location_detail

urlpatterns = [
    path('', location_list, name='location_list'),
    path('<int:pk>/', location_detail, name='location_detail'),
]
