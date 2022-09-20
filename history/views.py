import json
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from main.functions import custom_render

from history.models import HistoryItem
from main.constants import COUNT_PRODUCTS_ON_PAGE

class History(TemplateView):
    template_name = "history/products.html"

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect(reverse('products'))

        history = HistoryItem.objects.filter(user_id=request.user.id)

        paginator = Paginator(history, COUNT_PRODUCTS_ON_PAGE)
        page_obj = paginator.get_page(request.GET.get('page'))

        day = None
        is_first_page = True

        for item in page_obj:
            data = json.loads(item.data)
            item.total_cost = data["total_cost"]
            item.products = data["products"]
            item.time = item.created_at.time()

            date = item.created_at.date()

            if(is_first_page or date != day):
                item.date = date
                day = date

            is_first_page = False

        return custom_render(request, self.template_name, {
            'title' : 'History',
            'page_obj' : page_obj,
            'count' : len(history),
        })

