from decimal import Decimal

from django.contrib import admin
from django.db import models
from nested_inline.admin import NestedModelAdmin
from unfold import admin as unfold_admin
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from amiribd.core.admin import earnkraft_site

# Register your models here.
from amiribd.transactions.models import Transaction

from .forms import AdminAccountTypeForm
from .inlines import AccountInline
from .inlines import Plan
from .inlines import PoolFeatureInline
from .inlines import SavingInvestmentPlanInline
from .models import Account
from .models import AccountType
from .models import AccountWithdrawalAction
from .models import PlanType
from .models import Pool
from .models import PoolType
from .models import SavingPlan


@admin.register(Pool)
class PoolAdmin(NestedModelAdmin, ModelAdmin):
    list_display = [
        "profile",
        "account",
        "type",
        "created_at",
        "updated_at",
    ]
    inlines = [AccountInline, PoolFeatureInline]

    def delete_model(self, request, obj: Pool) -> None:
        if obj.profile:
            obj.profile.is_subscribed = False
            obj.profile.save()
        return super().delete_model(request, obj)


@admin.register(PoolType)
class PoolTypeAdmin(ModelAdmin):
    list_display = [
        "type",
        "price",
    ]


class PlanInlineAdmin(unfold_admin.StackedInline):
    model = Plan
    extra = 1


@admin.register(PlanType)
class PlanTypeAdmin(ModelAdmin):
    list_display = ["type", "price", "percentage_return", "icon", "svg"]

    inlines = [PlanInlineAdmin]
    formfield_overrides = {
        models.TextField: {
            "widgets": WysiwygWidget,
        },
    }


@admin.register(AccountType)
class AccountTypeAdmin(ModelAdmin):
    form = AdminAccountTypeForm
    list_display = [
        "type",
        "price",
    ]


@admin.register(Account, site=earnkraft_site)
class AccountAdmin(ModelAdmin):
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
        "locked_balance_account",
        "withdrawable_investment",
    ]

    def delete_model(self, request, obj: Account) -> None:
        if obj.pool.profile:
            obj.pool.profile.is_subscribed = False
            obj.pool.profile.save()
        return super().delete_model(request, obj)


@admin.register(Plan, site=earnkraft_site)
class PlanAdmin(ModelAdmin):
    list_display = [
        "account",
        "plan_profile_email",
        "plan_profile",
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
        "payment_method",
        "mpesa_transaction_code",
        "payment_phone_number",
        "is_paid",
    ]

    actions = [
        "verified_mpesa_code_transaction",
        "unverified_mpesa_code_transaction",
    ]
    list_filter = ["is_paid", "payment_method", "status"]
    search_fields = [
        "account__account_ssid",
        "mpesa_transaction_code",
    ]

    @admin.action(description="Mark selected as paid")
    def verified_mpesa_code_transaction(self, request, queryset):

        queryset.update(is_paid=True)

    @admin.action(description="Mark selected as unpaid")
    def unverified_mpesa_code_transaction(self, request, queryset):
        queryset.update(is_paid=False)


@admin.register(AccountWithdrawalAction, site=earnkraft_site)
class EventActionAdmin(ModelAdmin):
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
            # if not event.paid:
            #     Transaction.objects.create(
            #         profile=event.account.pool.profile,
            #         account=account,
            #         type="WITHDRAWAL",
            #         amount=event.amount,
            #         discount=0,
            #         paid=0,
            #         source="Admin Resolved Withdrawal",
            #         verified=True,
            #     )
        queryset.update(
            status="Resolved",
            paid=True,
        )

    @admin.action(description="Mark selected as Cancelled")
    def mark_as_cancelled(self, request, queryset):
        for event in queryset:
            if event.status != "Cancelled":
                account = Account.objects.get(id=event.account.id)
                account.balance += round((event.amount / Decimal("0.85")),2)
                account.save()
                Transaction.objects.create(
                    profile=event.account.pool.profile,
                    account=account,
                    type="DEPOSIT",
                    amount=event.amount,
                    discount=0,
                    paid=0,
                    source="Admin Cancelled Withdrawal",
                    verified=True,
                )
        queryset.update(status="Cancelled", paid=False)


@admin.register(SavingPlan)
class SavingPlanAdmin(ModelAdmin):
    list_display = [
        "title",
        "interest",
        "term",
        "principal",
        "amount",
        "earned_interest",
        "percentage_rate",
    ]

    inlines = [
        SavingInvestmentPlanInline,
    ]
