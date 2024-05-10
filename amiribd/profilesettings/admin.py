from django.contrib import admin

# Register your models here.
from .models import Notification, NotificationType, NotificationSubscription


class NotificationTypeInline(admin.StackedInline):
    model = NotificationType
    extra = 0


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [NotificationTypeInline]


@admin.register(NotificationSubscription)
class NotifyAdmin(admin.ModelAdmin):
    list_display = ("notify_label_type", "is_active")
