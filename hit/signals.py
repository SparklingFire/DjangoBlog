from articles.models import Article
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HitCount
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=Article)
def hitcount_model_save(sender, instance, **kwargs):
    try:
        instance.hitcount
    except ObjectDoesNotExist:
        HitCount.objects.create(article=instance)
