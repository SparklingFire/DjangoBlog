from django.db import models
from django.conf import settings
from django.utils import timezone
from tag.models import Tag


class BlackList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(default=timezone.now)

    def get_usernames(self):
        return self.blacklistedtag_set.values_list('user', flat=True)

    def __str__(self):
        return 'Черный список пользователя {0}'.format(self.user)


class BlackListedUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    anonymous_session = models.CharField(max_length=40, blank=True, null=True)
    blacklist = models.ForeignKey(BlackList, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Пользователь {0}, заблокированный у {1}'.format(self.user, self.blacklist.user)


class BlackListedTag(models.Model):
    blacklist = models.ForeignKey(BlackList, on_delete=models.CASCADE)
    tag = models.ObjectDoesNotExist(Tag)
    created = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Тэг {0}, заблокированный у {1}'.format(self.tag, self.blacklist.user)
