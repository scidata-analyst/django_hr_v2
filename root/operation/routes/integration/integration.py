from django.urls import path
from operation.views.integration.integration import integration

urlpatterns = [
    path('', integration, name='integration'),
]
