import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from APIStripe.models import Item

from favorites.models import FavoritesItem
from main.callback import render_button_ajax_modal_svg


class Favorites(TemplateView):
    template_name = "favorites/products.html"

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect(reverse('products'))

        html = ""
        count_products = 0

        ids = FavoritesItem.getIds(user_id=request.user.id)

        if ids:
            products = Item.objects.filter(id__in=ids)

            for item in products:

                html += render_to_string('favorites/item.html', {
                    'item' : item,
                    'delete' : render_button_ajax_modal_svg(
                        request=request, 
                        modal_id="delete_favorites",
                        svg="#main--res_svg--delete",
                        svg_classes="ico",
                        classes="favorite-delete btn",
                        rerender_always=True,
                        run_after_init="question.init()",
                        params={
                            "question" : "Do you want to remove an item from your favorites?",
                            "id" : str(item.id),
                            "name" : item.name,
                            "price" : str(item.price),
                            "f_yes" : "favorites.deleteFromFavorite()"
                            }
                        )
                })

            if products:
                count_products = len(products)

        return render(request, self.template_name, {
            'products' : html,
            'count_type' : count_products
            })


class Change(View):
    __ADD_TO_FAFORITE = "on"

    def post(self, request, *args, **kwargs):

        data_post = json.load(request)

        product_id = data_post["productId"]
        type_change = data_post["typeChange"]

        user_id = request.user.id

        ids = FavoritesItem.getIds(user_id=user_id)
        
        if type_change == self.__ADD_TO_FAFORITE:
            ids.append(product_id)
        else:
            ids.remove(product_id)

        if FavoritesItem.setIds(user_id, ids):
            status = 'success'
        else:
            status = 'failed'


        return JsonResponse({
            'type': str(type_change),
            'status': status
        })


class Delete(View):

    def post(self, request, *args, **kwargs):

        data_post = json.load(request)
        product_id = data_post["productId"]

        user_id = request.user.id

        ids = FavoritesItem.getIds(user_id=user_id)
        ids.remove(product_id)

        if FavoritesItem.setIds(user_id, ids):
            status = 'success'
        else:
            status = 'failed'


        return JsonResponse({
            'status': status
        })