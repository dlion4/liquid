from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from amiribd.invest.models import Account
from amiribd.transactions.models import Transaction
from amiribd.core.admin import earnkraft_site


# Register your models here.
from .models import WhatsAppEarningScheme


@admin.register(WhatsAppEarningScheme, site=earnkraft_site)
class WhatsAppEarningSchemeAdmin(admin.ModelAdmin):
    list_display = [
        "profile",
        "file",
        "created_at",
        "updated_at",
        "approved",
        "rejected",
        "rejected_at",
        "price",
        "amount",
    ]
    list_filter = [
        "approved",
        "rejected",
    ]

    actions = [
        "approve_views_and_credit_account",
        "reject_views_and_debit_account",
    ]

    # def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
    #     return WhatsAppEarningScheme.objects.select_related("profile").exclude(rejected=True)

    @admin.action(description="approved views and credit account")
    def approve_views_and_credit_account(self, request, queryset):
        queryset.update(approved=True, rejected=False)

        for obj in queryset.select_related("profile"):
            profile = obj.profile
            try:
                account = Account.objects.get(pool__profile=profile)
                account.balance += obj.amount
                account.save()

                Transaction.objects.create(
                    profile=profile,
                    account=account,
                    type="DEPOSIT",
                    amount=obj.amount,
                    discount=0,
                    source="WhatsAppEarningScheme Views Approval",
                )
            except Account.DoesNotExist:
                pass

    @admin.action(description="reject views and debit account")
    def reject_views_and_debit_account(self, request, queryset):
        queryset.update(approved=False, rejected=True)

        for obj in queryset.select_related("profile"):
            profile = obj.profile
            account = Account.objects.get(pool__profile=profile)

            try:
                transaction = Transaction.objects.filter(
                    profile=profile,
                    account=account,
                    source="WhatsAppEarningScheme Views Approval",
                    type="DEPOSIT",
                ).latest()

                account.balance -= obj.amount
                account.save()

                Transaction.objects.create(
                    profile=profile,
                    account=account,
                    type="WITHDRAWAL",
                    amount=obj.amount,
                    discount=0,
                    source="WhatsAppEarningScheme Views Rejections",
                )
            except Transaction.DoesNotExist:
                pass
