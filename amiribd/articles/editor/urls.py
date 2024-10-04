from django.urls import include
from django.urls import path

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
        "ai/new/",
        views.ArticleAiCreationView.as_view(),
        name="new-article-ai-generation-post",
    ),
    path(
        "new-article-ai-edit/<pk>/<slug>/",
        views.ContentAiEditPostView.as_view(),
        name="new-article-ai-edit",
    ),
    path(
        "youtube-summarizer/",
        views.YoutubeSummarizerView.as_view(),
        name="youtube-summarizer",
    ),
    path(
        "audio-transcription/",
        views.AudioTranscriptionView.as_view(),
        name="transcription",
    ),
    path(
        "transcript-summarization/",
        views.SummarizeTranscriptionView.as_view(),
        name="summarize",
    ),
    # article minor edits
    path(
        "htmx/",
        include("amiribd.articles.editor.htmx.urls", namespace="article_minor_edits"),
    ),
]
