from django.urls import path, include
from django.views.generic import RedirectView
from operation.views.api import operation_api

urlpatterns = [
    path('branding/', include('operation.routes.branding.branding')),
    path('compliance/', include('operation.routes.compliance.compliance')),
    path('global/', include('operation.routes.global.global')),
    path('health/', include('operation.routes.health.health')),
    path('integrations/', include('operation.routes.integration.integration')),
    path('integration/', RedirectView.as_view(pattern_name='integration', permanent=False)),
    path('reports/', include('operation.routes.report.report')),
    path('report/', RedirectView.as_view(pattern_name='report', permanent=False)),
    path('api/benefit-plan/', operation_api.benefit_plan_list, name='benefit_plan_list'),
    path('api/benefit-plan/<int:pk>/', operation_api.benefit_plan_detail, name='benefit_plan_detail'),
    path('api/benefit-enrollment/', operation_api.benefit_enrollment_list, name='benefit_enrollment_list'),
    path('api/safety-incident/', operation_api.safety_incident_list, name='safety_incident_list'),
    path('api/safety-incident/<int:pk>/resolve/', operation_api.safety_incident_resolve, name='safety_incident_resolve'),
    path('api/policy/', operation_api.policy_list, name='policy_list'),
    path('api/policy/<int:pk>/', operation_api.policy_detail, name='policy_detail'),
    path('api/policy/<int:pk>/acknowledge/', operation_api.policy_acknowledge, name='policy_acknowledge'),
    path('api/compliance/', operation_api.compliance_list, name='compliance_list'),
    path('api/compliance/<int:pk>/complete/', operation_api.compliance_complete, name='compliance_complete'),
    path('api/report/headcount/', operation_api.report_headcount, name='report_headcount'),
    path('api/report/attendance/', operation_api.report_attendance, name='report_attendance'),
    path('api/report/turnover/', operation_api.report_turnover, name='report_turnover'),
    path('api/integration/', operation_api.integration_list, name='integration_list'),
    path('api/integration/<int:pk>/toggle/', operation_api.integration_toggle, name='integration_toggle'),
]
