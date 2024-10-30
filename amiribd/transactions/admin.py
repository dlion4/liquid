from django.contrib import admin  # noqa: I001
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from amiribd.core.admin import earnkraft_site
from django.core.exceptions import ValidationError
from django.db import DatabaseError

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
    list_filter = [
        "source",
        "type",
        "verified",
        "is_payment_success",
        "currency",
    ]
    actions = ["verify_transaction_and_update_account"]

    @admin.action(description="Verify and Update Transaction")
    def verify_transaction_and_update_account(self, request, queryset):
        """
        Admin action to verify selected transactions and update account balances accordingly.
        """
        success_count = 0
        failure_count = 0
        for transaction in queryset:
            try:
                # Ensure transaction is not already verified
                if not transaction.verified:
                    transaction.verify_transaction()
                    transaction.save()
                    success_count += 1
                else:
                    self.message_user(
                        request,
                        f"Transaction {transaction.id} is already verified.",
                        level="warning",
                    )
            except ValidationError as e:
                failure_count += 1
                self.message_user(
                    request,
                    f"Validation error for transaction {transaction.id}: {e}",
                    level="error",
                )
            except DatabaseError as e:
                failure_count += 1
                self.message_user(
                    request,
                    f"Database error for transaction {transaction.id}: {e}",
                    level="error",
                )
            except Exception as e:  # noqa: BLE001
                # Catch-all for any other exceptions not specifically handled
                failure_count += 1
                self.message_user(
                    request,
                    f"An unexpected error occurred for transaction {transaction.id}: {e}",
                    level="error",
                )

        # Provide feedback to admin
        if success_count:
            self.message_user(
                request,
                f"Successfully verified {success_count} transaction(s).",
            )
        if failure_count:
            self.message_user(
                request,
                f"{failure_count} transaction(s) failed to verify.",
                level="error",
            )
