from django.urls import include
from django.urls import path

from amiribd.articles.editor.views import ContentArticleUpdateView

from . import views

app_name = "articles"

urlpatterns = [
    path("content/", views.BloggingHomeView.as_view(), name="blogging-home"),
    path("templates/", views.BloggingTemplateView.as_view(), name="blogging-templates"),
    path(
        "history/posts/",
        views.PostHistoryListView.as_view(),
        name="blogging-posts-history",
    ),
    path(
        "blogging/available-plans-for-ai/",
        views.PricingPlanForAiBloggingView.as_view(),
        name="blogging-with-ai-pricing-plan",
    ),
    path(
        "payment/payment-for-plans-for-ai/",
        views.PaymentPlanForAiView.as_view(),
        name="payment-for-plans-for-ai",
    ),
    path(
        "articles/<tm__year>/<tm__month>/<tm__day>/<slug>/",
        views.ArticleDetailView.as_view(),
        name="article-detail",
    ),
    path(
        "articles/<tm__year>/<tm__month>/<tm__day>/<slug>/edit/",
        ContentArticleUpdateView.as_view(),
        name="article-detail-edit",
    ),
    # include the editor url
    path("editor/", include("amiribd.articles.editor.urls", namespace="editor")),
]
