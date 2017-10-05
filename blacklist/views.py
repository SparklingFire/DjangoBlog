from custom_user.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from .models import BlackListedUser
from django.http import JsonResponse


def blacklist_user(request, target):
    if request.user.is_authenticated() is False:
        return JsonResponse({'error': 'только зарегистрированные юзеры могут добавлять в черный список'})
    user = CustomUser.objects.get(username=target)
    message = {}
    if request.user == user:
        message.update({'message': 'вы не можете занести в черный список сами себя'})
    else:
        try:
            BlackListedUser.objects.get(user=user).delete()
            message.update({'message': 'пользователь {0} разблокирован'.format(target), 'block': False})
        except ObjectDoesNotExist:
            BlackListedUser.objects.create(blacklist=request.user.blacklist,
                                           user=user)
            message.update({'message': 'пользователь {0} заблокирован'.format(target), 'block': True})
    return JsonResponse(message)
