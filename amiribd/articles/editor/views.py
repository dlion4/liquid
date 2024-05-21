from amiribd.articles.models import Article
from amiribd.articles.views import ArticleMixinView
from amiribd.articles.forms import ArticleForm
from django.shortcuts import get_object_or_404, redirect, render

# views.py

from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core.files.storage import default_storage
from django_ckeditor_5.views import upload_file

from amiribd.dashboard.views import DashboardViewMixin


class UploadFile(View):
    @method_decorator(csrf_exempt)
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

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if not form.is_valid():
            print(form.errors)
            return render(request, self.template_name, {"form": form})
        instance = form.save(commit=False)
        instance.profile = self.request.user.profile_user
        instance.save()
        return redirect(instance)


class ContentArticleUpdateView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/editor/editor.html"
    form_class = ArticleForm

    def get_object(self, **kwargs):
        return get_object_or_404(
            Article,
            profile=self.get_profile(),
            slug=self.kwargs.get("slug"),
            created_at__year=self.kwargs.get("tm__year"),
            created_at__month=self.kwargs.get("tm__month"),
            created_at__day=self.kwargs.get("tm__day"),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(instance=self.get_object(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            request.POST, request.FILES, instance=self.get_object(**kwargs)
        )
        if not form.is_valid():
            print(form.errors)
            return render(request, self.template_name, {"form": form})
        instance = form.save(commit=False)
        instance.profile = self.request.user.profile_user
        instance.save()
        return redirect(instance)


class ContentAiGeneratorView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/editor/generate.html"


class ContentAiEditPostView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/editor/edit.html"
