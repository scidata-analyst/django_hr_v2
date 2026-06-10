from django.urls import path
from talent_growth.views.talent.talent import talent
from talent_growth.views.api.talent_api import (
    talent_profile_list, succession_plan_list
)

urlpatterns = [
    path('', talent, name='talent'),
    path('api/profile/', talent_profile_list, name='talent_profile_list'),
    path('api/succession/', succession_plan_list, name='succession_plan_list'),
]
