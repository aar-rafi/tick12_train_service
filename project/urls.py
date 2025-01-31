from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),  # Include hello app's URLs
    path('', include('django_prometheus.urls')),
]

