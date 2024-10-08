import json

# Create your views here.
from django.conf import settings
from django.contrib.auth import get_user
from django.shortcuts import get_object_or_404

from amiribd.articles.models import Article
from amiribd.dashboard.views import DashboardViewMixin
from amiribd.invest.models import Account

additional_js_ckeditor_logic = """
    .then(editor => {
        window.editor = editor;

        const annotationsUIs = editor.plugins.get('AnnotationsUIs');
        const sidebarElement = document.querySelector('.sidebar');
        let currentWidth;

        function refreshDisplayMode() {
            if (window.innerWidth === currentWidth) {
                return;
            }
            currentWidth = window.innerWidth;

            if (currentWidth < 1000) {
                sidebarElement.classList.remove('narrow');
                sidebarElement.classList.add('hidden');
                annotationsUIs.switchTo('inline');
            } else if (currentWidth < 1300) {
                sidebarElement.classList.remove('hidden');
                sidebarElement.classList.add('narrow');
                annotationsUIs.switchTo('narrowSidebar');
            } else {
                sidebarElement.classList.remove('hidden', 'narrow');
                annotationsUIs.switchTo('wideSidebar');
            }
        }

        editor.ui.view.listenTo(window, 'resize', refreshDisplayMode);
        refreshDisplayMode();

        return editor;
    })
    .catch(error => {
        console.error('There was a problem initializing the editor.', error);
    });
"""


class ArticleMixinView(DashboardViewMixin):
    queryset = Account
    def get_profile(self):
        return get_user(self.request).profile_user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ckeditor_config"] = json.dumps(settings.CKEDITOR_5_CONFIGS)
        context["additional_js_ckeditor_logic"] = additional_js_ckeditor_logic
        context["articles"] = (
            Article.objects.prefetch_related("profile")
            .filter(profile=self.get_profile())
            .order_by("-created_at")
        )
        return context


class BloggingHomeView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/home.html"


class BloggingTemplateView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/templates.html"


class PostHistoryListView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/posts.html"


class PricingPlanForAiBloggingView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/pricing.html"


class PaymentPlanForAiView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/payment.html"


class ArticleDetailView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/article_detail.html"
    queryset = Account

    def get_article_object(self, **kwargs):
        return get_object_or_404(
            Article,
            slug=self.kwargs.get("slug"),
            created_at__year=self.kwargs.get("tm__year"),
            created_at__month=self.kwargs.get("tm__month"),
            created_at__day=self.kwargs.get("tm__day"),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["article"] = self.get_article_object(**kwargs)
        return context
