from django.shortcuts import redirect, HttpResponseRedirect
from .models import (Vote)
from comments.models import Comment
from articles.models import Article
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from utils_tags_cp.utils import get_ip


def vote_builder(rating_model, user, like, request):
    try:
        vote = Vote.objects.get(rating_model=rating_model,
                                user=user)
        if vote.like == like:
            vote.delete()
        else:
            vote.like = like
            vote.save()

    except ObjectDoesNotExist:
        Vote.objects.create(session=request.session.session_key,
                            ip=get_ip(request),
                            like=like,
                            rating_model=rating_model,
                            user=user)

    rating_model.calculate_score()
    if request.is_ajax():
        return JsonResponse({'likes': str(rating_model.likes),
                             'dislikes': str(rating_model.dislikes),
                             'like': like})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def comment_rating_view(request, pk, vote):
    if request.user.is_authenticated() is False:
        return JsonResponse({'error': 'оценивать комментарии могу только зарегистрированные пользователи'})
    like = True if vote == 'like' else False

    try:
        rating_model = Comment.objects.get(pk=pk).get_rating_model()
    except ObjectDoesNotExist:
        redirect('gag')
    user = request.user

    return vote_builder(rating_model, user, like, request)


def article_rating_view(request, pk, vote):
    if request.user.is_authenticated() is False:
        return JsonResponse({'error': 'оценивать новость могу только зарегистрированные пользователи'})
    like = True if vote == 'like' else False

    try:
        rating_model = Article.objects.get(pk=pk).get_rating_model()
    except ObjectDoesNotExist:
        redirect('gag')

    user = request.user

    return vote_builder(rating_model, user, like, request)
