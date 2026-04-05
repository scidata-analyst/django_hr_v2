from django.urls import path

from main.views import home

urlpatterns = [
    path("dashboard/", home, name="home"),
    path("", home, name="home"),
]
