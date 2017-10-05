from tag.models import Tag
from articles.forms import SearchForm
from articles.models import Article
from comments.models import Comment


def popular_articles(request):
    articles = Article.objects.get_popular_articles()[:5]
    return {'POPULAR_ARTICLES': articles}


def tag_list(request):
    tags = Tag.objects.all()
    return {"TAGS": tags}


def search_form(request):
    form = SearchForm
    return {"SEARCH_FORM": form}


def recent_comments(request):
    return {"RECENT_COMMENTS": Comment.objects.recent_comments()}