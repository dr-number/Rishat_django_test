from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=18, decimal_places=2)

    def get_price(self):
        return str(self.price)
    
