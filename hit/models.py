from django.db import models
from articles.models import Article


class HitCount(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    hits = models.SmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now_add=True)

    def add_hit(self):
        self.hits += 1
        self.save()

    def remove_hit(self):
        self.hits -= 1
        self.save()


class Hit(models.Model):
    created = models.DateTimeField(editable=False, auto_now_add=True, db_index=True)
    edited = models.DateTimeField(editable=False, auto_now_add=True)
    ip = models.CharField(max_length=40, editable=False)
    session = models.CharField(max_length=40, editable=False)
    hitcount = models.ForeignKey(HitCount, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.hitcount.add_hit()
        super().save(*args, **kwargs)

    def remove(self):
        self.hitcount.remove_hit()
        self.delete()
