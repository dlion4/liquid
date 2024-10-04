from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold import admin as unfold_admin

# Register your models here.
from .models import (
    Inbox, 
    Room, 
    RoomMessage, 
    Favorite, 
    Message, 
    Archive, 
    AdminInbox, 
    Notification,
    # this is for test and learning the redis realtime communitions and annonimous async message broadcasting
    Post
)


class RoomMessageInline(unfold_admin.StackedInline):
    model = RoomMessage
    extra = 0


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("owner", "kind", "name", "slug", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}

    prepopulated_fields = {"slug": ("name",)}

    inlines = [RoomMessageInline]


@admin.register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ("profile",)
    search_fields = ("profile", "rooms")


class ArchiveInline(unfold_admin.StackedInline):
    model = Archive
    extra = 0


class InboxMessageInline(unfold_admin.StackedInline):
    model = Inbox
    extra = 0


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ("sender", "receiver", "created_at", "updated_at")
    search_fields = ("sender", "receiver")
    list_filter = ("created_at", "updated_at")
    list_display_links = ("sender", "receiver")

    inlines = [
        ArchiveInline,
        InboxMessageInline,
    ]


@admin.register(AdminInbox)
class AdminInboxAdmin(ModelAdmin):
    list_display = [
        "message",
    ]

@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ['title']


@admin.register(Post)
class PostPlayAdmin(ModelAdmin):
    list_display = ['title']