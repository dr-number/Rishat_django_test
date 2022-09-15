from django.conf.urls import include
from django.urls import path

from favorites.views import (
    Favorites,
    Change,
    Delete
)



urlpatterns = [
    path('', Favorites.as_view(), name='favorites'),
    path('change', Change.as_view(), name='favorites_change'),
    path('delete', Delete.as_view(), name='favorites_delete'),
]