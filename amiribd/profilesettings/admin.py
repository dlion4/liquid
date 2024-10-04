from django.contrib import admin
from unfold import admin as unfold_admin
# Register your models here.
from .models import Notification, NotificationType, NotificationSubscription
from amiribd.core.admin import earnkraft_site
from django.db import models
from unfold.widgets import UnfoldAdminTextInputWidget, UnfoldBooleanSwitchWidget
from unfold.contrib.forms.widgets import WysiwygWidget

class NotificationTypeInline(unfold_admin.StackedInline):
    model = NotificationType
    extra = 0
    formfield_overrides = {
        models.BooleanField : {
            "widget": UnfoldBooleanSwitchWidget,
        }
    }

@admin.register(Notification, site=earnkraft_site)
class NotificationAdmin(unfold_admin.ModelAdmin):
    list_display = ("title",)
    inlines = [NotificationTypeInline]
    formfield_overrides = {
        "description" : {"widget": WysiwygWidget}
    }


@admin.register(NotificationSubscription)
class NotifyAdmin(unfold_admin.ModelAdmin):
    list_display = ("notify_label_type", "is_active")
