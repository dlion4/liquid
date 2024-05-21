from amiribd.users.models import Profile
from amiribd.articles.models import Article
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from django.http import HttpResponse, JsonResponse

# from django.db import
from django.utils.decorators import method_decorator


class ArticleRealTimeAjaxCreateView(View):
    @method_decorator(csrf_exempt)
    async def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
