from django.conf.urls import include
from django.urls import path


from custom_user.views import (
    authorization
    )



urlpatterns = [
    path('authorization/', authorization, name='authorization'),
    # path('authorization/', Change.as_view(), name='authorization'),
]