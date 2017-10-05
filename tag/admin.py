from django.contrib import admin
from .models import Tag
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


class TagExtend(admin.ModelAdmin):
    def save_related(self, request, form, formsets, change):
        try:
            pos_copy = Tag.objects.filter(tag=form.instance.tag)
        except ObjectDoesNotExist:
            pos_copy = None

        super().save_related(request, form, formsets, change)
        obj = form.instance

        if pos_copy:
            for post in obj.article.all():
                pos_copy[0].article.add(post)
                pos_copy[0].edited = timezone.now()
            pos_copy[0].save()
            if len(pos_copy) >= 2:
                obj.delete()

    list_display = ('__str__', 'created', 'edited')


admin.site.register(Tag, TagExtend)