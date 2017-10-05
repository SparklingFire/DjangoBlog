from django.db.models.signals import post_save
from django.dispatch import receiver
from custom_user.models import CustomUser
from . import models


@receiver(signal=post_save, sender=CustomUser)
def create_blacklist(sender, instance, *args, **kwargs):
    models.BlackList.objects.get_or_create(user=instance)
