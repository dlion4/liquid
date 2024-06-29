from django.contrib import admin

# Register your models here.
from .models import JobApplication, Job
from .forms import AddJobForm
from amiribd.core.admin import earnkraft_site
from unfold.admin import ModelAdmin
from django.db import models
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold import admin as unfold_admin
from unfold.widgets import UnfoldAdminTextInputWidget, UnfoldBooleanSwitchWidget

class JobApplicationInlineAdmin(unfold_admin.StackedInline):
    model = JobApplication
    extra = 0
    formfield_overrides={
        models.CharField:{
            "widget":UnfoldAdminTextInputWidget
        },
        models.TextField:{
            "widget":WysiwygWidget
        },
    }


@admin.register(Job, site=earnkraft_site)
class JobAdmin(ModelAdmin):
    
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
    
    formfield_overrides = {
        models.TextField:{
            "widget":WysiwygWidget
        },
        models.BooleanField: {
            'widget':UnfoldBooleanSwitchWidget
        }               
    }
