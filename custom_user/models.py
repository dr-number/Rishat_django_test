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

class TemporaryBanIp(models.Model):
    ip_address = models.GenericIPAddressField("IP address")
    attempts = models.IntegerField("Failed attempts", default=0)
    time_unblock = models.DateTimeField("Time ban", blank=True)
    status = models.BooleanField("Status ban", default=False)
 
    def __str__(self):
        return self.ip_address

