from django.urls import path, include

urlpatterns = [
    path('engagement/', include('talent_growth.routes.engagement.engagement')),
    path('performance/', include('talent_growth.routes.performance.performance')),
    path('training/', include('talent_growth.routes.training.training')),
    path('talent/', include('talent_growth.routes.talent.talent')),
]
