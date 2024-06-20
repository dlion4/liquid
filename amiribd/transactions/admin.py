from django.contrib import admin

# Register your models here.
from .models import PaymentMethod, Transaction


@admin.register(PaymentMethod)
class PaymentMethod(admin.ModelAdmin):
    list_display = [
        "channel",
    ]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
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
