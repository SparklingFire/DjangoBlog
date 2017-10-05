from django.conf.urls import url
from user_messages import views


urlpatterns = [
    url(regex='^get_chat_list_data/$',
        view=views.chat_list_loader_refresh,
        name='chat-refresh'),

    url(regex='^chat_list/(?P<filter>[\w]+)/$',
        view=views.load_chat_list_page,
        name='chat-list-loader'),

    url(regex='^chat_room/(?P<pk>[\w]+)/$',
        view=views.chat_room,
        name='chat-room'),

    url(regex='^send_chat_message/(?P<pk>[\w]+)/$',
        view=views.ChatSendMessage.as_view(),
        name='send-chat-message')
]
