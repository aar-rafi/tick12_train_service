from django.urls import path
from .views import get_train_names_view

urlpatterns = [
    path('api/trains/get', get_train_names_view, name='get_train_names'),
    # Other URLs
]

