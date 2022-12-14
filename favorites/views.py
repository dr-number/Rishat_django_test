import json
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from APIStripe.models import Item

from favorites.models import FavoritesItem
from main.functions import custom_render

from django.core.paginator import Paginator
from main.callback import prepare_params
from main.constants import COUNT_PRODUCTS_ON_PAGE
from main.functions import ModelJsonData


class RenderDeleteButton():
    def render(self, item: Item) -> set:
        button = {
            "modal_id": "delete_favorites",
            "svg": "#main--res_svg--delete",
            "svg_classes": "ico",
            "classes": "favorite-delete btn",
            "rerender_always": "1",
            "run_after_init": "question.init()",
            "app_name": "favorites",
            "params": ""
        }

        from_modals_params = {
            "f_yes": "favorites.deleteFromFavorite()",
            "id": str(item.id),
            "name": item.name,
            "price": str(item.price)
        }

        button["params"] = prepare_params(from_modals_params)
        return button


class Favorites(TemplateView):
    template_name = "favorites/products.html"

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect(reverse('products'))

        modelJsonData = ModelJsonData()

        count_products = 0
        ids = modelJsonData.get_data(FavoritesItem, request.user.id, 'products_id')

        if not ids:
            return custom_render(request, self.template_name, {
                'title' : 'Favorites'
            })

        products = Item.objects.filter(id__in=ids)
       
        count_products = len(products)
        paginator = Paginator(products, COUNT_PRODUCTS_ON_PAGE)
        page_obj = paginator.get_page(request.GET.get('page'))

        renderDeleteButton = RenderDeleteButton()
        
        for item in page_obj:
            item.data_delete = renderDeleteButton.render(item)

        return custom_render(request, self.template_name, {
            'title' : 'Favorites',
            'page_obj' : page_obj,
            'count_type' : count_products
            })


class Change(View):
    __ADD_TO_FAFORITE = "on"

    def post(self, request, *args, **kwargs):

        data_post = json.load(request)

        product_id = data_post["productId"]
        type_change = data_post["typeChange"]

        user_id = request.user.id

        modelJsonData = ModelJsonData()
        ids = modelJsonData.get_data(FavoritesItem, user_id, 'products_id')
        
        if type_change == self.__ADD_TO_FAFORITE:
            ids.append(product_id)
        else:
            ids.remove(product_id)

        if modelJsonData.set_data(FavoritesItem, user_id, 'products_id', ids):
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

        modelJsonData = ModelJsonData()

        ids = modelJsonData.get_data(FavoritesItem, user_id, 'products_id')
        ids.remove(product_id)

        if modelJsonData.set_data(FavoritesItem, user_id, 'products_id', ids):
            status = 'success'
        else:
            status = 'failed'


        return JsonResponse({
            'status': status
        })