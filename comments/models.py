from django.db import models
from django.conf import settings
from articles.models import Article
from rating.models import RatingModel
from django.contrib.contenttypes.fields import GenericRelation
import datetime


class CommentsManager(models.Manager):
    def recent_comments(self):
        return Comment.objects.order_by('-created')[:5]


class Comment(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()
    day = models.DateField(default=datetime.date.today(), editable=False)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               editable=False
                               )
    session = models.CharField(max_length=40, editable=False)
    ip = models.CharField(max_length=40, editable=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    target_name = models.CharField(max_length=50, null=True, blank=True)
    name = models.TextField(editable=False)
    rating_object = GenericRelation(RatingModel)
    published = models.BooleanField(default=False)
    objects = CommentsManager()

    def get_likes(self):
        return self.rating_object.only('likes').last().likes

    def get_dislikes(self):
        return self.rating_object.only('dislikes').last().dislikes

    def get_rating_model_pk(self):
        return self.rating_object.only('id').last().id

    def get_rating_model(self):
        return self.rating_object.last()

    def get_avatar(self):
        if self.author:
            return self.author.get_avatar()
        else:
            return None

    def save(self, *args, **kwargs):
        try:
            self.name = '#' + str(Comment.objects.last().id + 1)
        except:
            super().save(*args, **kwargs)
            self.name = '#1'
        if self.parent:
            self.target_name = self.parent.name
            if self.parent.parent:
                self.parent = self.parent.parent
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.article.get_absolute_url()

    def __str__(self):
        return 'Comment ID: {0}'.format(self.id)

    def get_like_color(self, user):
        try:
            return self.get_rating_model().vote_set.get(user=user).like
        except models.ObjectDoesNotExist:
            return None

    def get_user_info_text(self):
        return 'оставил комментарий в теме {0}'.format(self.article.title)
