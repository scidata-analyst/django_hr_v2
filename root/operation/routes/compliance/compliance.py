from django.urls import path
from operation.views.compliance.compliance import compliance

urlpatterns = [
    path('', compliance, name='compliance'),
]
