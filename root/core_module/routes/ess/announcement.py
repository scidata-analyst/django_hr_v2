from django.urls import path
from core_module.views.api.ess.announcement import announcement_list

urlpatterns = [
    path('', announcement_list, name='announcement_list'),
]
