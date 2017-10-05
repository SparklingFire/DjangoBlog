from django.contrib import admin
from .models import BlackList, BlackListedUser


class BlackListExtension(admin.ModelAdmin):
    list_display = ('user', 'created', 'edited')


class BlackListedUserExtension(admin.ModelAdmin):
    list_display = ('user', 'blacklist', 'created', 'edited', 'anonymous_session')

admin.site.register(BlackList, BlackListExtension)
admin.site.register(BlackListedUser, BlackListedUserExtension)
