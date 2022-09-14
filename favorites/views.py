import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse

from favorites.models import FavoritesItem


class Favorites(TemplateView):
    template_name = "favorites/products.html"

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect(reverse('products'))

        products = FavoritesItem.objects.filter(user_id=request.user.id)

        html = ""

        for item in products:

            html += render_to_string('favorites/item.html', {
                'item' : item
            })

        return render(request, self.template_name, {
            'products' : html,
            'count_type' : len(products)
            })


class Change(View):
    __ADD_TO_FAFORITE = "on"

    def post(self, request, *args, **kwargs):

        data_post = json.load(request)
        product_id = data_post["productId"]
        type_change = data_post["typeChange"]

        favorites = FavoritesItem.objects.filter(id=request.user.id).values('products_id').first()
        ids = FavoritesItem.getIds(favorites)

        if type_change == self.__ADD_TO_FAFORITE:
            ids.append(product_id)
        else:
            ids.remove(product_id)

        if FavoritesItem.setIds(request.user.id, ids):
            status = 'success'
        else:
            status = 'failed'


        return JsonResponse({
            'type': str(type_change),
            'status': status
        })
