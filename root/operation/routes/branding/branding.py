from django.urls import path
from operation.views.branding.branding import branding

urlpatterns = [
    path('', branding, name='branding'),
]
