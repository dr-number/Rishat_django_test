from django.contrib import admin
from history.models import HistoryItem

class CustomerHistoryItem(admin.ModelAdmin):
    list_display = ("user_name", "status", "currency", "created_at")

admin.site.register(HistoryItem, CustomerHistoryItem)
