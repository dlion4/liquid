from django.urls import path


from . import views


app_name = "article_minor_edits"

urlpatterns = [
    # path("<int:pk>/", views.ArticleEditView.as_view(), name="article-edit"),
    # path("<int:pk>/delete/", views.ArticleDeleteView.as_view(), name="article-delete"),
    # path(
    #     "<int:pk>/publish/", views.ArticlePublishView.as_view(), name="article-publish"
    # ),
    # path("<int:pk>/unpublish/", views.ArticleUnpublishView.as_view, name="article"),
    path("edit-create-title/", views.update_article_title_view, name="create-edit-title"),
]
