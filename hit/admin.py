from django.contrib import admin
from .models import (Hit, HitCount)


class HitExtension(admin.ModelAdmin):
    list_display = ('ip', 'session', 'created', 'edited')


class HitCountExtension(admin.ModelAdmin):
    list_display = ('article', 'hits', 'created', 'edited')


admin.site.register(Hit, HitExtension)
admin.site.register(HitCount)
