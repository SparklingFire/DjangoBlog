from django.db import models
from articles.models import Article
from django.conf import settings


class Tag(models.Model):
    article = models.ManyToManyField(Article)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now_add=True, editable=False)
    tag = models.CharField(max_length=25)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)

    @staticmethod
    def get_articles_by_tag(tag):
        return Tag.objects.get(tag=tag).article.all()

    def __str__(self):
        return self.tag
