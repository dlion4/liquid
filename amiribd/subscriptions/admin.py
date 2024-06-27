from django.contrib import admin  # Register your models here.
from .models import Issue
from .forms import AdminIssueForm

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ["profile", "title", "created_at", "resolved", "files"]
    form = AdminIssueForm
    list_filter = [
       "profile",
       "resolved",
    ]
