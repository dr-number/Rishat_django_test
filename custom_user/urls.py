from django.urls import path


from custom_user.views import (
    Registration,
    Authorization,
    Signout,
    BanIpPage
    )


urlpatterns = [
    path('registration/', Registration.as_view(), name='registration'),
    path('authorization/', Authorization.as_view(), name='authorization'),
    path('signout/', Signout.as_view(), name='signout'),
    path('banIpPage/?time=banSmall', BanIpPage.as_view(), name='banSmall'),
    path('banIpPage/?time=banLong', BanIpPage.as_view(), name='banLong'),
]