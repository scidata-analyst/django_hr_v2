"""
URL configuration for root project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # Include URLs from the main app
    path('core-module/', include('core_module.urls')),  # Include URLs from the core module app
    path('talent-growth/', include('talent_growth.urls')),  # Include URLs from the talent growth app
    path('operation/', include('operation.urls')),  # Include URLs from the operation app
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
