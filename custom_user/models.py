from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from user_messages.models import Message
from django.utils import timezone
from articles.models import Subscription, Article
from django.contrib.contenttypes.fields import GenericRelation
from utils_tags_cp.models import Image
from django.conf import settings
from django.core.cache import cache
import datetime
from Blog_01 import settings
from user_messages.models import ChatRoom
from django.db.models import Sum, Prefetch, Count


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Введите адрес электронной почты')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            password=password
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=25, unique=True)
    username_slug = models.CharField(max_length=25, blank=True, null=True, unique=True)
    email = models.EmailField()
    birthday = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False, verbose_name='activation')
    is_admin = models.BooleanField(default=False, verbose_name='Admin permission')
    objects = CustomUserManager()
    avatar = GenericRelation(Image)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        self.username_slug = self.username.lower()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_user_rating_object(self):
        return self.userratingmodel

    def get_subscription_articles(self):
        return self.get_subscriptions().values_list('article', flat=True)

    def get_unread_subscription_counter(self):
        result = self.get_subscriptions().aggregate(Sum('new_comments')).get('new_comments__sum')
        return 0 if result is None else result

    def update_subscriptions(self):
        for sub in self.get_subscriptions():
            sub.get_updates()

    def get_subscriptions(self):
        return self.subscription_set.all()

    def get_user_articles(self):
        return self.article_set.all()

    def get_user_comments(self):
        return self.comment_set.all()

    def get_user_tag(self):
        return self.tag_set.all()

    def get_user_rating(self):
        return self.get_user_rating_object().score

    def get_user_likes(self):
        return self.get_user_rating_object().likes

    def get_user_dislikes(self):
        return self.get_user_rating_object().dislikes

    def get_user_unread_messages(self, current_room=None):
        chat_rooms = ChatRoom.objects.filter(users=self).exclude(pk=current_room).prefetch_related(
            Prefetch('message_set',
                     queryset=Message.objects.filter(check=False).exclude(user=self),
                     to_attr='unread_messages')
        )
        return sum([len(x.unread_messages) for x in chat_rooms])

    def get_avatar(self):
        return self.avatar.last().image.url

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def get_blacklist(self):
        pass

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                    seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False
