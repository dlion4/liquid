from django.contrib import admin
from .models import Payment, PaystackPaymentStatus
from amiribd.core.admin import earnkraft_site
# Register your models here.


@admin.register(Payment, site=earnkraft_site)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "channel", "account", "created_at", "updated_at")


@admin.register(PaystackPaymentStatus, site=earnkraft_site)
class PaystackPaymentStatusAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "status",
        "reference",
        "amount",
        "created_at",
        "updated_at",
    ]