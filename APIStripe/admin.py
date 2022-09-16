from django.contrib import admin

from APIStripe.models import CurrencyItem, Item

class CustomerCurrencyItem(admin.ModelAdmin):
    list_display = ("currency", )

class CustomerItem(admin.ModelAdmin):
    list_display = ("name", "description", "price")


admin.site.register(Item, CustomerItem)
admin.site.register(CurrencyItem, CustomerCurrencyItem)


