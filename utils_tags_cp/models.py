from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Image(models.Model):
    image = models.ImageField(upload_to='media/images/')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='tied object')
    object_id = models.SlugField()
    content_object = GenericForeignKey('content_type', 'object_id')
