from amiribd.articles.views import ArticleMixinView
from amiribd.articles.forms import ArticleForm

# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core.files.storage import default_storage
from django_ckeditor_5.views import upload_file


class UploadFile(View):
    @method_decorator(csrf_exempt, name="dispatch")
    def post(self, request, *args, **kwargs):
        upload_view = upload_file
        return upload_view(request, *args, **kwargs)


ck_editor_upload_files = UploadFile.as_view()


class ContentCreationEditorView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/editor/editor.html"
    form_class = ArticleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context


class ContentAiGeneratorView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/editor/generate.html"


class ContentAiEditPostView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/editor/edit.html"
