from django.urls import path, include
from . import views

app_name = "editor"

urlpatterns = [
    path("new-article/", views.ContentCreationEditorView.as_view(), name="new-article"),
    path(
        "new-article-ai-generation/",
        views.ContentAiGeneratorView.as_view(),
        name="new-article-ai-generation",
    ),
    path(
        "new-article-ai-edit/",
        views.ContentAiEditPostView.as_view(),
        name="new-article-ai-edit",
    ),
    # articel minor edits
    path(
        "htmx/",
        include("amiribd.articles.editor.htmx.urls", namespace="article_minor_edits"),
    ),
]