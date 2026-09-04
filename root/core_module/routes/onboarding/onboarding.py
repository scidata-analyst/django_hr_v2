from django.urls import path, include
from core_module.views.onboarding.onboarding import onboarding

urlpatterns = [
    path('', onboarding, name='onboarding'),
    path('api/task/', include('core_module.routes.onboarding.onboarding_task')),
    path('api/offboarding/', include('core_module.routes.onboarding.offboarding')),
    path('api/exit-interview/', include('core_module.routes.onboarding.exit_interview')),
]
