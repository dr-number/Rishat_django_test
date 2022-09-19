from cgitb import text
from django.db import models

class HistoryItem(models.Model):
    user_id = models.IntegerField()
    data = models.JSONField(null=True)
    currency = models.CharField(max_length=6, default="usd")
    status = models.CharField(max_length=20, default="expectation")
    created_at = models.DateTimeField(auto_now_add=True)
