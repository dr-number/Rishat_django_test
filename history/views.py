import json
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.paginator import Paginator

from history.models import HistoryItem
from main.constants import COUNT_PRODUCTS_ON_PAGE

class History(TemplateView):
    template_name = "history/products.html"

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect(reverse('products'))

        day = None
        history = HistoryItem.objects.filter(user_id=request.user.id)

        for item in history:
            data = json.loads(item.data)
            item.total_cost = data["total_cost"]
            item.products = data["products"]
            item.time = item.created_at.time()

            date = item.created_at.date()

            if(date != day):
                item.date = date
                day = date

        paginator = Paginator(history, COUNT_PRODUCTS_ON_PAGE)
        page_obj = paginator.get_page(request.GET.get('page'))

        return render(request, self.template_name, {
            'title' : 'History',
            'page_obj' : page_obj,
            'count' : len(history),
        })

