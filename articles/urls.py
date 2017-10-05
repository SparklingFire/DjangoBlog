from django.conf.urls import url
from . import views


urlpatterns = [
    url(regex='^$',
        view=views.ArticlesList.as_view(),
        name='article-list'),

    url(regex='^article/(?P<pk>[-\w ]+)/$',
        view=views.ArticleDetails.as_view(),
        name='article-details'),

    url(regex='^error/$',
        view=views.ErrorGag.as_view(),
        name='gag'),

    url(regex='^site_info/$',
        view=views.SiteInfo.as_view(),
        name='site-info'),

    url(regex='^contacts/$',
        view=views.Contacts.as_view(),
        name='contacts'),

    url(regex='^filter/tag/(?P<tag>[-\w ]+)/$',
        view=views.ArticlesList.as_view(),
        name='article-list'),

    url(regex='^subscribe/(?P<primary_key>[-\w ]+)/$',
        view=views.SubscriptionManagement.as_view(),
        name='subscribe'),

    url(regex='^comment/delete/(?P<pk>[0-9]+)/$',
        view=views.delete_comment,
        name='delete-comment'),

    url(regex='^delete_subscription/(?P<pk>[0-9]+)/$',
        view=views.delete_subscription,
        name='delete-subscription'),

    url(regex='^create_article/$',
        view=views.create_article,
        name='create-article'),

    url(regex='^update_article/(?P<pk>[-\w ]+)/$',
        view=views.update_article,
        name='update-article'),

    url(regex='^delete_article/(?P<article_pk>[-\w ]+)/$',
        view=views.delete_article,
        name='article-delete'),

    url(regex='^load_comments/(?P<article_pk>[-\w]+)/$',
        view=views.load_comments,
        name='load-comments'),

    url(regex='^edit_comment/(?P<pk>[-\w]+)/$',
        view=views.edit_comment,
        name='edit-comments')
]
