from django.contrib import admin

# Register your models here.
from .models import Post
from .forms import PostForm
from amiribd.core.admin import earnkraft_site
from unfold.admin import ModelAdmin


@admin.register(Post, site=earnkraft_site)
class PostAdmin(ModelAdmin):
    pass

