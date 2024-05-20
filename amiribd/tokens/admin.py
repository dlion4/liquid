from django.contrib import admin

from amiribd.tokens.models import AuthToken, Token


# Register your models here.
@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "is_active")
    list_filter = ("is_active",)
    search_fields = ("user__username",)


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "is_active")
    list_filter = ("is_active",)
    search_fields = ("user__username",)
