from django.urls import path, include
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

    # include the editor url
    path("editor/", include("amiribd.articles.editor.urls", namespace="editor"))
]
