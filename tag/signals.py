from articles.models import Article
from django.db.models.signals import (pre_delete)
from .models import Tag
from django.dispatch import receiver


@receiver(pre_delete, sender=Article)
def delete_empty_tags(sender, instance, **kwargs):
    tags = instance.get_article_tags()
    for tag in tags:
        if tag.article.all().count() == 1:
            tag.delete()
