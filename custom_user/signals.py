from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from custom_user.models import UserCustom

@receiver(post_save, sender=User)
def create_custom_user(sender, instance, created, **kwargs):
    if created:
        UserCustom.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_custom_user(sender, instance, **kwargs):
    instance.custom_user.save()