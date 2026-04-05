from django.urls import path
from operation.views.report.report import report

urlpatterns = [
    path('', report, name='report'),
]
