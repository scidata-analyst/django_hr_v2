from django.urls import path
from talent_growth.views.performance.performance import performance
from talent_growth.views.api.performance_api import (
    performance_review_list, performance_review_complete,
    goal_list, goal_update_progress
)

urlpatterns = [
    path('', performance, name='performance'),
    path('api/review/', performance_review_list, name='performance_review_list'),
    path('api/review/<int:pk>/complete/', performance_review_complete, name='performance_review_complete'),
    path('api/goal/', goal_list, name='goal_list'),
    path('api/goal/<int:pk>/progress/', goal_update_progress, name='goal_update_progress'),
]
