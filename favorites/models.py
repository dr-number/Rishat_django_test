from django.db import models

class FavoritesItem(models.Model):
    user_id = models.IntegerField()
    products_id = models.JSONField(null=True)

