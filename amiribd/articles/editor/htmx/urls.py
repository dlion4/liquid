from django.urls import path

from . import views

app_name = "article_minor_edits"

urlpatterns = [
    path(
        "edit-create-title/", views.update_article_title_view, name="create-edit-title",
    ),
]
