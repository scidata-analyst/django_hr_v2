/**
 * @module routes/employee/employee
 * @description Employee module root routes
 */

from django.urls import path, include
from core_module.views.employee.employee import employee, employee_detail, employee_create, employee_update, employee_delete

urlpatterns = [
    path('', employee, name='employee'),
    path('<int:id>/', employee_detail, name='employee_detail'),
    path('create/', employee_create, name='employee_create'),
    path('update/<int:id>/', employee_update, name='employee_update'),
    path('delete/<int:id>/', employee_delete, name='employee_delete'),
    path('api/department/', include('core_module.routes.employee.department')),
    path('api/location/', include('core_module.routes.employee.location')),
    path('api/designation/', include('core_module.routes.employee.designation')),
    path('api/employee/', include('core_module.routes.employee.employee_api')),
    path('api/document/', include('core_module.routes.employee.document')),
]
