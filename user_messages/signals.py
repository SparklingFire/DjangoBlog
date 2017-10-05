from custom_user.models import CustomUser
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from .models import (Message, ChatRoom)
from django.db.models import Q


@receiver(pre_delete, sender=Message)
def check_message_room(sender, instance, **kwargs):
    message_room = instance.message_room
    if message_room.message_set.all().count() == 1:
        message_room.delete()
    return instance
