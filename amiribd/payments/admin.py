from django.contrib import admin
from .models import Payment, PaystackPaymentStatus

# Register your models here.


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "channel", "account", "created_at", "updated_at")


@admin.register(PaystackPaymentStatus)
class PaystackPaymentStatusAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "status",
        "reference",
        "amount",
        "created_at",
        "updated_at",
    ]