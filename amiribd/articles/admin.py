
from django.contrib import admin

# Register your models here.
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.widgets import UnfoldAdminTextInputWidget
from unfold.widgets import UnfoldBooleanSwitchWidget

from amiribd.articles.editor.ai.models import AIHistory
from amiribd.core.admin import earnkraft_site

from .models import Article
from .models import Template
from .models import TemplateCategory
from .models import YtSummarizer

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
    list_display = [
        "title", "views", "archived", "reads",
        "trending", "popular", "editorsPick", "sponsored"]
    prepopulated_fields = {"slug": ("title",)}
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
            "widget": UnfoldBooleanSwitchWidget,
        },
    }


@admin.register(Template, site=earnkraft_site)
class TemplateAdmin(ModelAdmin):
    list_display = ["category"]


@admin.register(TemplateCategory, site=earnkraft_site)
class TemplateCategoryAdmin(ModelAdmin):
    list_display = ["title", "timestamp", "is_new", "templates_count"]
    inlines = []


@admin.register(AIHistory, site=earnkraft_site)
class AIHistoryAdmin(ModelAdmin):
    list_display = ["title", "created_at"]
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
    }


@admin.register(YtSummarizer, site=earnkraft_site)
class YtSummarizerAdmin(ModelAdmin):
    list_display = [
        "profile",
        "video_url",
        "timestamp",
        "summary",
        "audio_url",
        "is_processed",
    ]
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
    }
