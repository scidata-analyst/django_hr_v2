from operation.views.global_view.global_view import global_view
from operation.views.api.global_api import office_list, office_detail
from django.urls import path

urlpatterns = [
    path('', global_view, name='global_view'),
    path('api/office/', office_list, name='office_list'),
    path('api/office/<int:pk>/', office_detail, name='office_detail'),
]
