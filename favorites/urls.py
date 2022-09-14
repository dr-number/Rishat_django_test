from django.conf.urls import include
from django.urls import path

from favorites.views import (
    Favorites,
    Change
)



urlpatterns = [
    path('', Favorites.as_view(), name='favorites'),
    path('change', Change.as_view(), name='favorites_change'),
]