from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


class UserRatingModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def calculate_score(self):
        child_rating_objects = self.ratingmodel_set.all()
        likes = child_rating_objects.aggregate(models.Sum('likes'))
        dislikes = child_rating_objects.aggregate(models.Sum('dislikes'))
        self.likes = likes['likes__sum']
        self.dislikes = dislikes['dislikes__sum']
        self.score = self.likes - self.dislikes
        self.save()


class RatingModel(models.Model):
    user_rating_model = models.ForeignKey(UserRatingModel, on_delete=models.CASCADE, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='tied object')
    object_id = models.SlugField()
    content_object = GenericForeignKey('content_type', 'object_id')

    score = models.SmallIntegerField(default=0)
    likes = models.SmallIntegerField(default=0)
    dislikes = models.SmallIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now, editable=False)
    edited = models.DateTimeField(default=timezone.now, editable=False)

    def get_related_article(self):
        return self.article

    def calculate_score(self):
        self.likes = self.vote_set.filter(like=True).count()
        self.dislikes = self.vote_set.filter(like=False).count()

        self.score = self.likes - self.dislikes
        self.save()

    def __str__(self):
        return "{0} {1}".format(self.content_type, self.object_id)


class Vote(models.Model):
    like = models.BooleanField(default=True)
    rating_model = models.ForeignKey(RatingModel, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False)
    edited = models.DateTimeField(default=timezone.now, editable=False)
    session = models.CharField(max_length=40, editable=False)
    ip = models.CharField(max_length=40, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
