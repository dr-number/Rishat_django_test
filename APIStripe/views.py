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
from history.functions_history import HISTORY_STATUS_CANCEL, HISTORY_STATUS_SUCCESS, prepare_array, prepare_data, set_history, update_status
from history.views import History
from main.callback import render_button_ajax_modal
from main.constants import COUNT_PRODUCTS_ON_PAGE
from main.functions import ModelJsonData

stripe.api_key = settings.STRIPE_SECRET_KEY

class RenderBuyButton:

    def render_from_basket(self, request):

        return render_button_ajax_modal(
            request=request,
            modal_id="select_curently",
            text="buy",
            classes="btn btn-success",
            rerender_always="1",
            run_after_init="initSelectCurentlyBasket()"
        )

    def render(self, request, item):

        select_curently_params = {
            "id" : str(item.id),
            "name" : item.name,
            "price" : str(item.price),
        }

        return render_button_ajax_modal(
            request=request,
            modal_id="select_curently",
            text="buy",
            classes="btn btn-success",
            rerender_always="1",
            params=select_curently_params,
            run_after_init="initSelectCurently()"
        )

class BasketCreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):

        try:
            data_post = json.load(request)
            data = data_post['data']
            currently = data[0]['price_data']['currency']

            history_id = None

            if(request.user.is_authenticated):
                history_id = set_history(request.user.id, prepare_array(data), currently)


            session = stripe.checkout.Session.create(
                line_items = data,
                mode = 'payment',
                success_url = request.META['HTTP_ORIGIN'] + '/success/?id=' + str(history_id),
                cancel_url = request.META['HTTP_ORIGIN'] + '/cancel/?id=' + str(history_id)
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
            currently = data_get["currently"]
            quantity = 1

            history_id = None

            if(request.user.is_authenticated):
                data_history = prepare_data(item.name, item.price, quantity)
                history_id = set_history(user_id=request.user.id, data=data_history, currently=currently)

            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': currently,
                        'product_data': {
                        'name': item.name,
                        },
                        'unit_amount': round(item.price * 100),
                    },
                    'quantity': quantity,
                }],
                mode = 'payment',
                success_url = request.META['HTTP_REFERER'] + 'success/?id=' + str(history_id),
                cancel_url = request.META['HTTP_REFERER'] + 'cancel/?id=' + str(history_id),
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

    def get(self, request, *args, **kwargs):
        if(request.user.is_authenticated):
            update_status(request.GET["id"], HISTORY_STATUS_SUCCESS)

        return render(request, self.template_name, {
            'title' : 'Success'
        })

class Cancel(TemplateView):
    template_name = "APIStripe/cancel.html"

    def get(self, request, *args, **kwargs):
        if(request.user.is_authenticated):
            update_status(request.GET["id"], HISTORY_STATUS_CANCEL)

        return render(request, self.template_name, {
            'title' : 'Cancel'
        })


class ProductItem(TemplateView):
    template_name = "APIStripe/item.html"

    def get(self, request, id, *args, **kwargs):
        item = Item.objects.get(pk = id)

        return render(request, self.template_name, {
            "item" : item
        })


class Products(TemplateView):
    template_name = "APIStripe/products.html"

    def get(self, request, *args, **kwargs):

        favorites = None
        is_authenticated = request.user.is_authenticated

        products = Item.objects.all()
        renderBuyButton = RenderBuyButton()

        modelJsonData = ModelJsonData()

        if is_authenticated:
            favorites = modelJsonData.get_data(FavoritesItem, request.user.id, 'products_id')

        paginator = Paginator(products, COUNT_PRODUCTS_ON_PAGE)
        page_obj = paginator.get_page(request.GET.get('page'))

        for item in page_obj:

            item.is_authenticated = is_authenticated

            if favorites and (len(favorites) == 0 or str(item.id) in favorites): 
                item.status_favorites = 'off'
                item.status_favorites_style = 'on'
            else:
                item.status_favorites = 'on'
                item.status_favorites_style = 'off'

            item.buy_html = renderBuyButton.render(request, item)

        countrySpec = CountrySpec()
        currencies = countrySpec.get_data()

        return render(request, self.template_name, {
            'title' : 'Products',
            'page_obj' : page_obj,
            'count' : len(products),
            'currencies' : currencies
            })


class CountrySpec():
    __CACHE_NAME = 'payment_currencies'
    __TTL = 1000 * 60 * 60 * 24 * 30

    def __get_result(self, currencies):

        currencies = currencies.replace("[", "").replace("]", "")
        currencies = currencies.replace('\"', "")
        currencies = currencies.split(", ")

        return json.dumps({
            "currencies": currencies
        })

    def get_data(self):

        payment_currencies = cache.get(self.__CACHE_NAME)
        
        if payment_currencies:
            return self.__get_result(payment_currencies)

        data = stripe.CountrySpec.retrieve("US")
        payment_currencies = data["supported_payment_currencies"]

        if not payment_currencies:
            return None

        cache.set(self.__CACHE_NAME, json.dumps(payment_currencies), self.__TTL)
        return self.__get_result(payment_currencies)


