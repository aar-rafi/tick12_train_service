from django.urls import path
from .views import get_train_names

urlpatterns = [
    path('', get_train_names, name='get_train_names'),
    # Other URLs
]

