from django.contrib import admin
from .models import Article
from .forms import AdminArticleForm
from amiribd.core.admin import earnkraft_site

# Register your models here.


@admin.register(Article, site=earnkraft_site)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title"]
    form = AdminArticleForm
    # prepopulated_fields = {"slug": ("title",)}
