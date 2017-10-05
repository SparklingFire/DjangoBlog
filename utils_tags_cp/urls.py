from django.conf.urls import url
from utils_tags_cp import views


urlpatterns = [
    url(regex='^update_user_info/$',
        view=views.update_user_info,
        name='update-user-info')
]