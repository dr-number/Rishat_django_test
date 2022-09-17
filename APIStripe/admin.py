from django.contrib import admin

from APIStripe.models import Item

class CustomerItem(admin.ModelAdmin):
    list_display = ("name", "description", "price")

admin.site.register(Item, CustomerItem)


