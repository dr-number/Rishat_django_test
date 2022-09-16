from django.conf.urls import include
from django.urls import path

from APIStripe.views import (
    Products,
    ProductItem,
    CreateCheckoutSessionView,
    Success,
    Cancel
)
from main.modals import (
    RenderModalAJAX,
    AutoUploadModals
)


urlpatterns = [
    path('', Products.as_view(), name='products'),
    path('success/', Success.as_view(), name='success'),
    path('cancel/', Cancel.as_view(), name='cancel'),
    path('item/<int:id>/', ProductItem.as_view(), name='buy'),
    path('buy/<int:id>/', CreateCheckoutSessionView.as_view(), name='item'),

    path('render_modal_ajax/', RenderModalAJAX.as_view(), name='render_modal_ajax'),
    path('auto_upload_modals/', AutoUploadModals.as_view(), name='auto_upload_modals')
]