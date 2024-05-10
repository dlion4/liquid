from django.contrib import admin

from amiribd.tokens.models import Token


# Register your models here.
@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "is_active")
    list_filter = ("is_active",)
    search_fields = ("user__username",)
