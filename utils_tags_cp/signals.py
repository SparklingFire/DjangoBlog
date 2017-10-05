from django.db.models.signals import post_save
from django.dispatch import receiver
from articles.models import Article


@receiver(post_save, sender=Article)
def image_handler(sender, instance, **kwargs):
    pass