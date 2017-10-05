from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from user_messages.models import Message, ChatRoom
from user_messages.forms import SendMessageForm
from custom_user.models import CustomUser
from django.db import transaction
from django.utils import formats
import json


def chat_room_generator(chat_room, user):
    last_message = chat_room_last_message(chat_room)
    receiver_user = [x for x in chat_room.users.all() if x != user][0]
    room_data = {'username': receiver_user.username,
                 'created': formats.date_format(last_message.created, "d M h:i"),
                 'last_message': last_message.text,
                 'update_info': last_message.pk,
                 'user_image': receiver_user.get_avatar(),
                 'check': last_message.check,
                 'update': False,
                 'url': chat_room.get_absolute_url(),
                 'last_message_pk': last_message.pk
                 }
    if last_message.user != user:
        room_data.update({'last_message_user_image': last_message.user.get_avatar()})
    return room_data


def chat_message_generator(message):
    new_message = {'username': message.user.username,
                   'message_text': message.text,
                   'created': formats.date_format(message.created, "d M h:i"),
                   'user_image': message.user.get_avatar(),
                   'check': message.check,
                   'update': False
                   }
    return new_message


def update_chat_message(current_message, message):
    message.check = True
    message.save()
    current_message.update({'update': True})
    return current_message


def chat_room_last_message(chat_room):
    return chat_room.message_set.last()


def chat_room_update(current_chat_room, last_message, user):
    current_chat_room.update({'check': last_message.check,
                              'update': True,
                              'last_message_text': last_message.text,
                              'last_message_pk': last_message.pk})
    if last_message.user != user:
        current_chat_room.update({'last_message_user_image': last_message.user.get_avatar()})
    return current_chat_room


def chat_list_loader_refresh(request):
    if request.method == 'POST' and request.is_ajax:
        current_chat_room_list = json.loads(request.POST.get('data'))
        request_border = json.loads(request.POST.get('border'))
        database_chat_room_list = request.user.chatroom_set.all()
        total_objects = len(database_chat_room_list)
        database_chat_room_list = database_chat_room_list[request_border: min(total_objects, request_border + 50)]
        response_data = {}
        for chat_room in database_chat_room_list:
            this_pk = str(chat_room.pk)
            try:
                current_chat_room = current_chat_room_list[this_pk]
                if current_chat_room['last_message_pk'] != chat_room.message_set.last().pk:
                    response_data.update({this_pk: chat_room_update(current_chat_room,
                                                                    chat_room_last_message(chat_room),
                                                                    request.user)})
            except KeyError:
                response_data.update({this_pk: chat_room_generator(chat_room, request.user)})

        return JsonResponse({'chat_room_list': response_data, 'list_count': total_objects})


def load_chat_list_page(request, filter):
    return render(request, 'user_messages/message_list.html')


def chat_room(request, pk):
    current_room = ChatRoom.objects.get(pk=pk)

    with transaction.atomic():
        for message in current_room.message_set.exclude(user=request.user).filter(check=False):
            message.check = True
            message.save()

    if request.method == 'POST' and request.is_ajax:
        current_room = ChatRoom.objects.get(pk=pk)
        current_messages_list = json.loads(request.POST.get('data'))
        request_border = json.loads(request.POST.get('border'))
        database_messages_list = current_room.message_set.all()[::-1]
        total_objects = len(database_messages_list)
        database_messages_list = database_messages_list[request_border: min(total_objects, request_border + 50)]
        response_data = {}
        for message in database_messages_list:
            this_pk = str(message.pk)
            try:
                current_message = current_messages_list[this_pk]
                if current_message['check'] != message.check:
                    response_data.update({this_pk: update_chat_message(current_message, message)})
            except KeyError:
                response_data.update({this_pk: chat_message_generator(message)})
        return JsonResponse({'messages_list': response_data,
                             'total_objects': total_objects,
                             'user': request.user.username}
                            )
    return render(request, 'user_messages/message_room.html', context={'form': SendMessageForm})


class ChatSendMessage(generic.FormView):
    form_class = SendMessageForm
    template_name = 'user_messages/message_form.html'

    def __init__(self):
        self.chat_room = None
        super().__init__()

    def form_valid(self, form):
        message = Message.objects.create(user=self.request.user,
                                         message_room=self.chat_room,
                                         text=form.cleaned_data.get('text')
                                         )
        if self.request.is_ajax():
            return JsonResponse({'messages_list': {str(message.pk): chat_message_generator(message)},
                                 'user': self.request.user.username}
                                )
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'errors': form.errors})
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        self.chat_room = ChatRoom.objects.get(pk=kwargs.pop('pk'))
        return super().dispatch(request, *args, **kwargs)
