from django.contrib import admin
from .models import Article
from .forms import AdminArticleForm


# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title"]
    form = AdminArticleForm
    # prepopulated_fields = {"slug": ("title",)}
