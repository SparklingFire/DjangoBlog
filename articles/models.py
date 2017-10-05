from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
from django.shortcuts import reverse
from django.contrib.contenttypes.fields import GenericRelation
from rating.models import RatingModel
from django.db import IntegrityError
from utils_tags_cp.models import Image
import datetime

class ArticleManager(models.Manager):
    def get_popular_articles(self):
        return Article.objects.all().order_by('hitcount__hits').reverse()


class Article(models.Model):
    title = models.CharField(max_length=60, unique=True)
    text = models.TextField()
    day = models.DateField(default=datetime.date.today(), editable=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    edited = models.DateTimeField(default=timezone.now, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    primary_key = models.SlugField(primary_key=True, unique=True, max_length=100, editable=False)
    rating_object = GenericRelation(RatingModel)
    image_object = GenericRelation(Image)

    def save(self, *args, **kwargs):
        """
        create a primary key for the article before saving the object
        """
        if not self.primary_key:
            self.primary_key = slugify(self.title)
        super().save(*args, **kwargs)

    def get_hits(self):
        return self.hitcount.hits

    def get_likes(self):
        return self.rating_object.last().likes

    def get_dislikes(self):
        return self.rating_object.last().dislikes

    def get_rating_model_pk(self):
        return self.rating_object.last().pk

    def get_rating_model(self):
        return RatingModel.objects.get(pk=self.get_rating_model_pk())

    def get_article_tags(self):
        return self.tag_set.all()

    def get_absolute_url(self):
        return reverse('article-details', args=[str(self.primary_key)])

    def get_image(self):
        return self.image_object.last().image.url

    objects = ArticleManager()

    def __str__(self):
        return '{0}'.format(self.title)

    def get_user_info_text(self):
        return 'создал тему {0}'.format(self.title)


class Subscription(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    subscribed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    ip = models.CharField(max_length=40, editable=False)
    new_comments = models.SmallIntegerField(default=0)
    checked_comments = models.SmallIntegerField(default=0)
    total_comments = models.SmallIntegerField(default=0)

    def __str__(self):
        return 'Подписка на {0}'.format(self.article.title)
