from django.urls import path
from operation.views.health.health import health

urlpatterns = [
    path('', health, name='health'),
]
