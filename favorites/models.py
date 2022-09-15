import json
from django.db import models

class FavoritesItem(models.Model):
    user_id = models.IntegerField()
    products_id = models.JSONField(null=True)

    def getIds(user_id):
        favorites = FavoritesItem.objects.filter(user_id=user_id).values('products_id').first()

        if favorites:
            favorites = favorites.get('products_id')
            return json.loads(favorites)

        return []

    def setIds(user_id, array):
        
        if not array:
            return None

        updated_values = {
            'products_id' : json.dumps(list(dict.fromkeys(array)))
            }

        result = FavoritesItem.objects.update_or_create(
            user_id = user_id,
            defaults = updated_values
        )

        return result[0].pk

