from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from amiribd.core.admin import earnkraft_site

# Register your models here.
from .models import PaymentMethod
from .models import Transaction


@admin.register(PaymentMethod, site=earnkraft_site)
class PaymentMethod(UnfoldModelAdmin):
    list_display = [
        "channel",
    ]


@admin.register(Transaction, site=earnkraft_site)
class TransactionAdmin(UnfoldModelAdmin):
    list_display = [
        "profile",
        "account",
        "type",
        "created_at",
        "updated_at",
        "amount",
        "discount",
        "paid",
        "verified",
        "receipt_number",
        "source",
        "payment_phone",
        "is_payment_success",
        "mpesa_transaction_code",
        "payment_phone_number",
        "currency",
        "country",
    ]
