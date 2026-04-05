from django.urls import path
from talent_growth.views.performance.performance import performance
from talent_growth.views.api import talent_api

urlpatterns = [
    path('', performance, name='performance'),
    path('api/review/', talent_api.performance_review_list, name='performance_review_list'),
    path('api/review/<int:pk>/complete/', talent_api.performance_review_complete, name='performance_review_complete'),
    path('api/goal/', talent_api.goal_list, name='goal_list'),
    path('api/goal/<int:pk>/progress/', talent_api.goal_update_progress, name='goal_update_progress'),
]
