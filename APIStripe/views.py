import stripe
from django.shortcuts import render
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.core.cache import cache
import json


from APIStripe.models import Item
from favorites.models import FavoritesItem

from django.core.paginator import Paginator
from main.callback import render_button_ajax_modal
from main.constants import COUNT_PRODUCTS_ON_PAGE

from main.functions import getCurrentHost

stripe.api_key = settings.STRIPE_SECRET_KEY

class BasketCreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):

        try:
            data_post = json.load(request)

            session = stripe.checkout.Session.create(
                line_items = data_post['data'],
                mode = 'payment',
                success_url = request.META['HTTP_ORIGIN'] + '/success/',
                cancel_url = request.META['HTTP_ORIGIN'] + '/cancel/',
            )

            clears = []

            ids = data_post['ids']

            for id in ids:
                clears.append('product_' + id)

            cache.delete_many(clears)


            return JsonResponse({
                'id': session.id
            })

        except Exception as e:
            return JsonResponse({ 
                'error': str(e)
            })


class CreateCheckoutSessionView(View):
    def get(self, request, id, *args, **kwargs):

        item = Item.objects.get(pk = id)

        try:
            data_get = request.GET

            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': data_get["currently"],
                        'product_data': {
                        'name': item.name,
                        },
                        'unit_amount': round(item.price * 100),
                    },
                    'quantity': 1,
                }],
                mode = 'payment',
                success_url = request.META['HTTP_REFERER'] + 'success/',
                cancel_url = request.META['HTTP_REFERER'] + 'cancel/',
            )

            return JsonResponse({
                'id': session.id
            })

        except Exception as e:
            return JsonResponse({ 
                'error': str(e)
            })


class Success(TemplateView):
    template_name = "APIStripe/success.html"

class Cancel(TemplateView):
    template_name = "APIStripe/cancel.html"


class ProductItem(TemplateView):
    template_name = "APIStripe/item.html"

    def get(self, request, id, *args, **kwargs):
        item = Item.objects.get(pk = id)

        context = super(ProductItem, self).get_context_data(**kwargs)
        context.update({
            "item" : item
        })

        return context


class Products(TemplateView):
    template_name = "APIStripe/products.html"

    def get(self, request, *args, **kwargs):

        favorites = None
        is_authenticated = request.user.is_authenticated

        products = Item.objects.all()

        if is_authenticated:
            favorites = FavoritesItem.getIds(user_id=request.user.id)

        countrySpec = CountrySpec()
        currencies = countrySpec.getData()

        for item in products:

            item.is_authenticated = is_authenticated

            if favorites and (len(favorites) == 0 or str(item.id) in favorites): 
                item.status_favorites = 'off'
                item.status_favorites_style = 'on'
            else:
                item.status_favorites = 'on'
                item.status_favorites_style = 'off'

            
            select_curently_params = {
                "id" : str(item.id),
                "name" : item.name,
                "price" : str(item.price),
                "currencies" : currencies
            }

            buy_html = render_button_ajax_modal(
                request=request,
                modal_id="select_curently",
                text="buy",
                classes="btn btn-success",
                rerender_always="1",
                params=select_curently_params,
                run_after_init="ApiStripe.initCheckOut()"
            )

            item.buy_html = buy_html

        paginator = Paginator(products, COUNT_PRODUCTS_ON_PAGE)
        page_obj = paginator.get_page(request.GET.get('page'))


        return render(request, self.template_name, {
            'page_obj' : page_obj,
            'count' : len(products)
            })


class CountrySpec():
    CACHE_NAME = 'payment_currencies'
    TTL = 1000 * 60 * 60 * 24 * 30


    def getData(self):

        payment_currencies = cache.get(self.CACHE_NAME)
        
        if payment_currencies:
            return payment_currencies

        data = stripe.CountrySpec.retrieve("US")
        payment_currencies = data["supported_payment_currencies"]

        if not payment_currencies:
            return None

        cache.set(self.CACHE_NAME, json.dumps(payment_currencies), self.TTL)
        return payment_currencies


