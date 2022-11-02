from django.db import models
from django.contrib.auth.models import User

class HistoryItem(models.Model):
    user_id = models.IntegerField()
    data = models.JSONField(null=True)
    currency = models.CharField(max_length=6, default="usd")
    status = models.CharField(max_length=20, default="expectation")
    created_at = models.DateTimeField(auto_now_add=True)

    def __get_user(self):
        return User.objects.get(pk = self.user_id)
        
    def user_name(self):
        return self.__get_user().username
