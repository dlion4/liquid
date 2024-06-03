from django.contrib import admin

# Register your models here.
from .models import Inbox, Room, RoomMessage, Favorite, Message, Archive, AdminInbox


class RoomMessageInline(admin.StackedInline):
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


# @admin.register(RoomMessage)
# class RoomMessageAdmin(admin.ModelAdmin):
#     list_display = (
#         "room",
#         "profile",
#         "created_at",
#         "updated_at",
#     )
#     search_fields = ("room",)
#     list_filter = ("created_at", "updated_at")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("profile",)
    search_fields = ("profile", "rooms")


class ArchiveInline(admin.StackedInline):
    model = Archive
    extra = 0


class InboxMessageInline(admin.StackedInline):
    model = Inbox
    extra = 0


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "created_at", "updated_at")
    search_fields = ("sender", "receiver")
    list_filter = ("created_at", "updated_at")
    list_display_links = ("sender", "receiver")

    inlines = [
        ArchiveInline,
        InboxMessageInline,
    ]


@admin.register(AdminInbox)
class AdminInboxAdmin(admin.ModelAdmin):
    list_display = [
        "message",
    ]
