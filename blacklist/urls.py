from django.conf.urls import url
from . import views
from custom_user import views as user_views

urlpatterns = [
    url(regex='^block_user/(?P<target>[\w]+)/$',
        view=views.blacklist_user,
        name='blacklist-user'),

    url(regex='^(?P<username>[\w]+)/user_info/user_blacklist/$',
        view=user_views.UserInfoBlackList.as_view(),
        name='blacklist-info-user'),

]