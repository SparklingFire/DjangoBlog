from django.conf.urls import url
from comments import views


urlpatterns = [
    url('/update_comments/(?P<article_pk>[-w]+)',
        view=views.comment_refresh,
        name='comment-refresh')
]
