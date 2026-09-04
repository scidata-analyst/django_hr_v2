from django.urls import path
from core_module.views.api import ess_api

urlpatterns = [
    path('', ess_api.announcement_list, name='announcement_list'),
]
