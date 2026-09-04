from django.urls import path, include
from core_module.views.ess.ess import ess

urlpatterns = [
    path('', ess, name='ess'),
    path('api/expense/', include('core_module.routes.ess.expense')),
    path('api/announcement/', include('core_module.routes.ess.announcement')),
]
