from typing import Any
from django.contrib import admin
from django.forms import Form
from django.http import HttpRequest
from .models import Article, Template, TemplateCategory, YtSummarizer
from .forms import AdminArticleForm
from amiribd.core.admin import earnkraft_site
from unfold.admin import ModelAdmin
# from unfold.contrib.inlines import NonrelatedTabularInline
# Register your models here.
from django.db import models
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.widgets import UnfoldAdminTextInputWidget, UnfoldBooleanSwitchWidget
from amiribd.articles.editor.ai.models import AIHistory


"""
profile
title
slug
content
created_at
updated_at
"""


@admin.register(Article, site=earnkraft_site)
class ArticleAdmin(ModelAdmin):
    list_display = ["title", "views", "archived", "reads", "trending", "popular", "editorsPick", "sponsored"]
    # form = AdminArticleForm
    # prepopulated_fields = {"slug": ("title",)}
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False
    formfield_overrides = {
        models.CharField: {
            "widget": UnfoldAdminTextInputWidget,
        },
        models.TextField: {
            "widget": WysiwygWidget,
        },
        models.BooleanField: {
            "widget": UnfoldBooleanSwitchWidget
        }
    }


@admin.register(Template, site=earnkraft_site)
class TemplateAdmin(ModelAdmin):
    list_display = ['category',]


@admin.register(TemplateCategory, site=earnkraft_site)
class TemplateCategoryAdmin(ModelAdmin):
    list_display = ['title', 'timestamp', 'is_new', 'templates_count']
    inlines = []


@admin.register(AIHistory, site=earnkraft_site)
class AIHistoryAdmin(ModelAdmin):
    list_display = ['title', 'created_at']
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
    }


@admin.register(YtSummarizer, site=earnkraft_site)
class YtSummarizerAdmin(ModelAdmin):
    list_display = [
        'profile',
        'video_url',
        'timestamp',
        'summary',
        'audio_url',
        'is_processed'
    ]
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
