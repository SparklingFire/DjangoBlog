from django.http import JsonResponse
from articles.models import Subscription
import json
from user_messages.models import ChatRoom
from articles.models import Article


def update_user_info(request):
    if request.method == 'POST' and request.is_ajax:
        current_room = json.loads(request.POST.get('current_room'))
        current_thread = json.loads(request.POST.get('current_thread'))
        user = request.user
        data = {'user_rating': request.user.userratingmodel.score,
                'unread_messages': user.get_user_unread_messages(current_room),
                'username': user.username}
        data.update({'subscriptions': json.dumps({x.article.primary_key: x.new_comments for x
                                                  in Subscription.objects.filter(subscribed_user=request.user)})})
        return JsonResponse(data)
