from django.urls import path
from core_module.views.employee.employee import employee, employee_detail, employee_create, employee_update, employee_delete
from core_module.views.api import employee_api

urlpatterns = [
    path('', employee, name='employee'),
    path('<int:id>/', employee_detail, name='employee_detail'),
    path('create/', employee_create, name='employee_create'),
    path('update/<int:id>/', employee_update, name='employee_update'),
    path('delete/<int:id>/', employee_delete, name='employee_delete'),
    path('api/department/', employee_api.department_list, name='department_list'),
    path('api/department/<int:pk>/', employee_api.department_detail, name='department_detail'),
    path('api/location/', employee_api.location_list, name='location_list'),
    path('api/location/<int:pk>/', employee_api.location_detail, name='location_detail'),
    path('api/designation/', employee_api.designation_list, name='designation_list'),
    path('api/designation/<int:pk>/', employee_api.designation_detail, name='designation_detail'),
    path('api/employee/', employee_api.employee_list, name='employee_list'),
    path('api/employee/<int:pk>/', employee_api.employee_detail_api, name='employee_detail_api'),
    path('api/employee/stats/', employee_api.employee_stats, name='employee_stats'),
    path('api/document/', employee_api.document_list, name='document_list'),
]
