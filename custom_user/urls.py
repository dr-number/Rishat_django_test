from django.conf.urls import include
from django.urls import path


from custom_user.views import (
    Registration,
    Authorization,
    signout
    )


urlpatterns = [
    path('registration/', Registration.as_view(), name='registration'),
    path('authorization/', Authorization.as_view(), name='authorization'),
    path('signout/', signout, name='signout'),
]