from django.urls import path

from history.views import (
    History,
)



urlpatterns = [
    path('', History.as_view(), name='history'),
]