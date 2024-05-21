from django.shortcuts import get_object_or_404
from amiribd.users.models import Profile
from amiribd.articles.models import Article


def update_article_title_view(request):
    title = request.GET.get("title", None)
    pk = request.GET.get("pk", None)

    if pk is None:
        return None

    article = get_object_or_404(Article, pk=pk)

    article.title = title
    article.save()

    return True
