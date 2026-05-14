from django.urls import path, include

urlpatterns = [
    path('attendance/', include('core_module.routes.attendance.attendance')),
    path('employee/', include('core_module.routes.employee.employee')),
    path('ess/', include('core_module.routes.ess.ess')),
    path('onboarding/', include('core_module.routes.onboarding.onboarding')),
    path('payroll/', include('core_module.routes.payroll.payroll')),
    path('recruitment/', include('core_module.routes.recruitment.recruitment')),
]
