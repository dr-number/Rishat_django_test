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

        history = HistoryItem.objects.filter(user_id=request.user.id)

        for item in history:
            item.products = json.loads(item.data)

        paginator = Paginator(history, COUNT_PRODUCTS_ON_PAGE)
        page_obj = paginator.get_page(request.GET.get('page'))

        return render(request, self.template_name, {
            'title' : 'Products',
            'page_obj' : page_obj,
            'count' : len(history),
        })

