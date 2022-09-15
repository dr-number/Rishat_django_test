from django.conf.urls import include
from django.urls import path

from APIStripe.views import (
    Products,
    ProductItem,
    CreateCheckoutSessionView,
    Success,
    Cancel
)
from main import modals


urlpatterns = [
    path('', Products.as_view(), name='products'),
    path('success/', Success.as_view(), name='success'),
    path('cancel/', Cancel.as_view(), name='cancel'),
    path('item/<int:id>/', ProductItem.as_view(), name='buy'),
    path('buy/<int:id>/', CreateCheckoutSessionView.as_view(), name='item'),

    path('render_modal_ajax/', modals.render_modal_ajax, name='render_modal_ajax'),
    path('auto_upload_modals/', modals.auto_upload_modals, name='auto_upload_modals')
]