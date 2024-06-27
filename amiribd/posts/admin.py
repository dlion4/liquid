from django.contrib import admin

# Register your models here.
from .models import Post
from .forms import PostForm
from amiribd.core.admin import earnkraft_site



@admin.register(Post, site=earnkraft_site)
class PostAdmin(admin.ModelAdmin):
    form = PostForm

