from django.db import models

class FavoritesItem(models.Model):
    user_id = models.IntegerField()
    products_id = models.CharField(max_length=255, default="")

    def getIds(str):
        if not str:
            return []

        return str.split(':')

    def setIds(user_id, array):
        
        if not array:
            return None

        array = list(dict.fromkeys(array))

        favorits = FavoritesItem(
            user_id = user_id,
            products_id = list(dict.fromkeys(array)))

        favorits.save()
        return favorits.id

