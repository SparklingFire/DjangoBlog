from django.contrib import admin
from .models import (RatingModel, Vote, UserRatingModel)


class ArticleRatingModelExtension(admin.ModelAdmin):
    pass


class VoteExtension(admin.ModelAdmin):
    pass


admin.site.register(RatingModel, ArticleRatingModelExtension)
admin.site.register(Vote, VoteExtension)
admin.site.register(UserRatingModel)
