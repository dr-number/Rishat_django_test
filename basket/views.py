from django.core.cache import cache
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.paginator import Paginator
import json

from APIStripe.models import Item
from APIStripe.views import CountrySpec, RenderBuyButton

class Change(View):
    __ADD_TO_BASKET = "1"

    def post(self, request, *args, **kwargs):

        try:

            data_post = json.load(request)
            product_id = data_post["productId"]
            type_change = data_post["typeChange"]

            name_cache = 'product_' + product_id
            count_product = cache.get(name_cache)

            if count_product:
                count_product = int(count_product)
            else:
                count_product = 0


            if type_change == self.__ADD_TO_BASKET:
                count_product += 1
            else:
                count_product -= 1


            if count_product > 0:
                cache.set(name_cache, str(count_product), timeout=None)
            else:
                cache.delete(name_cache)

            return JsonResponse({
                'type': str(type_change),
                'count': str(count_product),
                'status': 'success'
            })

        except Exception as e:
            return JsonResponse({ 
                'error': str(e),
                'status': 'failed'
            })

class Basket(TemplateView):
    template_name = "basket/products.html"

    def get(self, request, *args, **kwargs):
        products = Item.objects.all()

        count_type = 0
        basket_products = []

        renderBuyButton = RenderBuyButton()

        for item in products:
            count_product = cache.get('product_' + str(item.id))

            if count_product:
                count_type += 1
                item.count = count_product
                basket_products.append(item)

        countrySpec = CountrySpec()
        currencies = countrySpec.get_data()

        return render(request, self.template_name, {
            "title" : "Basket",
            "products" : basket_products,
            "count_type" : count_type,
            "buy_html" : renderBuyButton.render_from_basket(request),
            "currencies" : currencies
        })
