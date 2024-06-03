from django.contrib import admin

from amiribd.transactions.models import Transaction
from .models import (
    Pool,
    PoolType,
    PlanType,
    AccountType,
    Account,
    AccountWithdrawalAction,
)
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
    list_display = ["type", "price", "percentage_return", "icon", "svg"]

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
        "invite_profit",
        "latest_invite_interest",
        "account_ssid",
    ]


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = [
        "account",
        "type",
        "min_amount",
        "max_amount",
        "fee",
        "slug",
        "sku",
        "percentage_return",
        "created_at",
        "updated_at",
        "status",
        "plan_profile",
        "payment_method",
        "mpesa_transaction_code",
        "payment_phone_number",
    ]

    actions = [
        "verified_mpesa_code_transaction",
        "unverified_mpesa_code_transaction",
    ]

    @admin.action(description="Mark selected as paid")
    def verified_mpesa_code_transaction(self, request, queryset):
        queryset.update(is_paid=True)

    @admin.action(description="Mark selected as unpaid")
    def unverified_mpesa_code_transaction(self, request, queryset):
        queryset.update(is_paid=False)


@admin.register(AccountWithdrawalAction)
class EventActionAdmin(admin.ModelAdmin):
    list_display = [
        "account",
        "action",
        "status",
        "amount",
        "channel",
        "created_at",
        "updated_at",
        "withdrawal_date",
        "withdrawal_time",
        "payment_phone_number",
        "paid",
    ]
    actions = [
        "mark_as_resolved",
        "mark_as_cancelled",
    ]

    list_filter = ["status", "paid"]

    @admin.action(description="Mark selected as Resolved")
    def mark_as_resolved(self, request, queryset):
        for event in queryset:
            # get the specif account related to this
            account = Account.objects.get(id=event.account.id)
            # then updated the status
            # create the transaction
            if not event.paid:
                Transaction.objects.create(
                    profile=event.account.pool.profile,
                    account=account,
                    type="WITHDRAWAL",
                    amount=event.amount,
                    discount=0,
                    paid=0,
                    source="Admin Resolved Withdrawal",
                    verified=True,
                )
        queryset.update(status="Resolved", paid=True)

    @admin.action(description="Mark selected as Cancelled")
    def mark_as_cancelled(self, request, queryset):
        for event in queryset:
            # get the specif account related to this
            if event.status != "Cancelled":
                account = Account.objects.get(id=event.account.id)
                account.balance += event.amount
                account.save()
                # create a transaction
                Transaction.objects.create(
                    profile=event.account.pool.profile,
                    account=account,
                    type="DEPOSIT",
                    amount=event.amount,
                    discount=0,
                    paid=0,
                    source="Admin Cancelled Withdrawal",
                )

            # then updated the status
        queryset.update(status="Cancelled", paid=False)
