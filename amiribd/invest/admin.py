from django.contrib import admin
from .models import Pool
from nested_inline.admin import NestedModelAdmin
from .inlines import AccountInline, PoolFeatureInline

# Register your models here.


@admin.register(Pool)
class PoolAdmin(NestedModelAdmin):
    list_display = [
        "profile",
        "type",
        "fee",
        "created_at",
        "updated_at",
    ]
    inlines = [AccountInline, PoolFeatureInline]
