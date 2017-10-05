from django.shortcuts import render, get_object_or_404, reverse, redirect, Http404
from django.contrib.auth import logout, login, authenticate
from django.views import generic
from django.views.generic.base import ContextMixin
from django.http import JsonResponse
from .forms import LoginForm
from .models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain
from collections import OrderedDict
from articles.models import Article
from comments.models import Comment
from django.utils import formats
import json


class LogoutView(generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return self.request.META.get('HTTP_REFERER','/')

    def dispatch(self, request, *args, **kwargs):
        logout(self.request)
        return super().dispatch(request, *args, **kwargs)


class LoginView(generic.FormView):
    form_class = LoginForm
    template_name = 'user/login.html'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')

    def form_invalid(self, form):
        if self.request.is_ajax:
            print(form.errors)
            return JsonResponse({'errors': form.errors})
        else:
            return super().form_invalid(form)

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        )
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(reverse('article-list'))
        return super().dispatch(request, *args, **kwargs)


class UserInfoView(generic.View):
    def __init__(self):
        self.user = None
        super().__init__()

    def build_activity(self, this_act):
        this_act_split = this_act.split(' ')
        this_act_id = this_act_split[1]
        this_act_type = this_act_split[0]
        if this_act_type == 'Article':
            obj = Article.objects.get(pk=this_act_id)
        else:

            obj = Comment.objects.get(pk=int(this_act_id))
        result = OrderedDict()
        result.update({this_act: {
                    'pk': this_act_id,
                    'username': obj.author.username,
                    'created': formats.date_format(obj.created, "h:i"),
                    'info': obj.get_user_info_text(),
                    'url': obj.get_absolute_url(),
                    'avatar': obj.author.get_avatar(),
                    'text': obj.text}
        })
        return result

    def post(self, request, username):
        current_activity_data = OrderedDict()
        current_activity_json = json.loads(request.POST.get('data'))
        request_border = json.loads(request.POST.get('border'))
        database_current_activity = sorted(list(self.user.article_set.all()) + list(self.user.comment_set.all()),
                                           key=lambda x: x.created)[::-1]
        total_objects = len(database_current_activity)
        database_current_activity = database_current_activity[request_border: min(total_objects, request_border + 50)]
        for act in database_current_activity:
            this_act = act.__class__.__name__ + ' ' + str(act.pk)
            day = formats.date_format(act.day, "M d")
            try:
                current_activity_json[day]
            except KeyError:
                try:
                    current_activity_data[day].update(self.build_activity(this_act))
                except KeyError:
                    current_activity_data.setdefault(day, self.build_activity(this_act))
        return JsonResponse({'data': current_activity_data,
                             'total_objects': total_objects,
                             'total_likes': self.user.get_user_likes(),
                             'total_dislikes': self.user.get_user_dislikes()
                             })

    def get(self, request, username):
        return render(request, 'user/user_info.html', context={'username': self.user.username,
                                                               'auth_user': self.request.user.username,
                                                               'avatar': self.user.get_avatar,
                                                               'created': self.user.birthday,
                                                               'likes': self.user.get_user_likes(),
                                                               'dislikes': self.user.get_user_dislikes(),
                                                               'button': 'черный список',
                                                               'title': 'текущая активность'})

    def dispatch(self, request, *args, **kwargs):
        self.user = CustomUser.objects.get(username=kwargs['username'])
        return super().dispatch(request, *args, **kwargs)


def check_auth(request):
    data = {}
    if request.is_ajax():
        if request.user.is_authenticated():
            data.update({'auth': 'true'})
        else:
            data.update({'auth': 'false'})
    return JsonResponse(data)


def change_avatar(request, username):
    try:
        CustomUser.objects.get(username=username)
    except ObjectDoesNotExist:
        pass


class UserInfoBlackList(generic.View):
    def __init__(self):
        self.user = None
        super().__init__()

    def post(self, request, username):
        current_blacklist = self.user.blacklist.blacklisteduser_set.all().prefetch_related('user')
        if self.request.is_ajax():
            return JsonResponse({'data': [bl.user.username for bl in current_blacklist]})

    def get(self, request, username):
        return render(request, 'user/user_info.html', context={'username': self.user.username,
                                                               'auth_user': self.request.user.username,
                                                               'avatar': self.user.get_avatar,
                                                               'created': self.user.birthday,
                                                               'likes': self.user.get_user_likes(),
                                                               'dislikes': self.user.get_user_dislikes(),
                                                               'button': 'текущая активность',
                                                               'title': 'черный список'})

    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        return super().dispatch(request, *args, **kwargs)
