from django.contrib import admin
from .models import Comment


class CommentExtension(admin.ModelAdmin):
    list_display = ('author', 'day', 'pk', 'created', 'edited', 'article')


admin.site.register(Comment, CommentExtension)
