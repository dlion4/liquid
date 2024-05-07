from django.contrib import admin
from .models import Pool, PoolType, PlanType, AccountType, Account
from nested_inline.admin import NestedModelAdmin
from .inlines import AccountInline, PoolFeatureInline, Plan

# Register your models here.


@admin.register(Pool)
class PoolAdmin(NestedModelAdmin):
    list_display = [
        "profile",
        "account",
        "type",
        "created_at",
        "updated_at",
    ]
    inlines = [AccountInline, PoolFeatureInline]


@admin.register(PoolType)
class PoolTypeAdmin(admin.ModelAdmin):
    list_display = [
        "type",
        "price",
    ]


class PlanInlineAdmin(admin.StackedInline):
    model = Plan
    extra = 1


@admin.register(PlanType)
class PlanTypeAdmin(admin.ModelAdmin):
    list_display = [
        "type",
        "price",
    ]

    inlines = [PlanInlineAdmin]


@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = [
        "type",
        "price",
    ]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        "account_owner",
        "pool",
        "type",
        "created_at",
        "updated_at",
        "balance",
    ]
