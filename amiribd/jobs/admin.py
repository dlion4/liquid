from django.contrib import admin

# Register your models here.
from .models import JobApplication, Job
from .forms import AddJobForm
from amiribd.core.admin import earnkraft_site

class JobApplicationInlineAdmin(admin.StackedInline):
    model = JobApplication
    extra = 0


@admin.register(Job, site=earnkraft_site)
class JobAdmin(admin.ModelAdmin):
    form = AddJobForm
    list_display = [
        "title",
        "location",
        "date_posted",
        "author",
        "is_popular",
        "job_applications",
        "is_new",
        "is_active",
        "location_type"
    ]
    search_fields = [
        'location',
        'title',
    ]
    list_filter = [
        'location',
        "is_active",
        "location_type"
    ]

    inlines = [
        JobApplicationInlineAdmin,
    ]