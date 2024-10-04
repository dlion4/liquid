from django.contrib import admin
from django.db import models
from unfold import admin as unfold_admin
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.widgets import UnfoldBooleanSwitchWidget

from amiribd.tokens.models import AuthToken
from amiribd.tokens.models import Secret
from amiribd.tokens.models import SecretCredential
from amiribd.tokens.models import Token


# Register your models here.
@admin.register(Token)
class TokenAdmin(ModelAdmin):
    list_display = ("user", "token", "is_active")
    list_filter = ("is_active",)
    search_fields = ("user__username",)


@admin.register(AuthToken)
class AuthTokenAdmin(ModelAdmin):
    list_display = ("user", "code", "is_active")
    list_filter = ("is_active",)
    search_fields = ("user__username",)


class SecretInline(unfold_admin.StackedInline):
    model = Secret
    formfield_overrides = {
        models.TextField:{
            "widget":WysiwygWidget,
        },
        models.BooleanField: {
            "widget": UnfoldBooleanSwitchWidget,
        },
    }
    extra = 0


@admin.register(SecretCredential)
class SecretCredentialAdmin(ModelAdmin):
    list_display = (
        "name","email","is_active", "created_at", "timesince",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    inlines = [
        SecretInline,
    ]




