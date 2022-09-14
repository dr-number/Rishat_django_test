from django.db import models
from django.contrib.auth.models import User

class UserCustom(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_user')
    description = models.CharField(max_length=255)
 
    def __unicode__(self):
        return self.user
 
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
