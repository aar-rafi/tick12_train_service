from django.urls import path
from .views import get_train_names_view

urlpatterns = [
    path('', get_train_names_view, name='get_train_names'),
    # Other URLs
]

