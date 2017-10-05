from django.conf.urls import url
from .views import comment_rating_view, article_rating_view

urlpatterns = [
    url('^comment/rate/(?P<pk>[0-9]+)/(?P<vote>[\w]+)/$',
        view=comment_rating_view,
        name='comment-like'),
    url('^article/rate/(?P<pk>[-\w]+)/(?P<vote>[\w]+)/$',
        view=article_rating_view,
        name='article-like'),
]
