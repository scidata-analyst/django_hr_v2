"""
@module routes/recruitment/recruitment
@description Recruitment module root routes
"""

from django.urls import path, include
from core_module.views.recruitment.recruitment import recruitment

urlpatterns = [
    path('', recruitment, name='recruitment'),
    path('api/job/', include('core_module.routes.recruitment.job')),
    path('api/candidate/', include('core_module.routes.recruitment.candidate')),
    path('api/interview/', include('core_module.routes.recruitment.interview')),
]
