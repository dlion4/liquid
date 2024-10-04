
# from django.db import
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


class ArticleRealTimeAjaxCreateView(View):
    @method_decorator(csrf_exempt)
    async def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
