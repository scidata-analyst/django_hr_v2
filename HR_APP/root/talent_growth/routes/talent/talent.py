from django.urls import path
from talent_growth.views.talent.talent import talent
from talent_growth.views.api import talent_api

urlpatterns = [
    path('', talent, name='talent'),
    path('api/profile/', talent_api.talent_profile_list, name='talent_profile_list'),
    path('api/succession/', talent_api.succession_plan_list, name='succession_plan_list'),
]
