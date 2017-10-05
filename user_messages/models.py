from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from django.conf import settings
from django.shortcuts import reverse


class ChatRoom(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(default=timezone.now)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return 'Комната {0}'.format(', '.join(x.username for x in self.users.all()))

    def last_message(self):
        return self.message_set.last()

    def get_absolute_url(self):
        return reverse('chat-room', args=[str(self.pk)])


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message_room = models.ForeignKey(ChatRoom)
    created = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    check = models.BooleanField(default=False)

    def __str__(self):
        return 'Сообщение от {0} в комнате {1}'.format(self.user, self.message_room)
