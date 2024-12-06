import uuid

from django.db import models
from django.db.models import OuterRef
from django.db.models import Q
from django.db.models import Subquery
from django.utils import timezone
from django.utils.functional import cached_property

from amiribd.invest.models import Plan
from amiribd.users.models import Profile

from .types import TransactionType


class TransactionQuerySet(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(Q(verified=True) & Q(is_payment_success=True))
        )


def generate_receipt_number():
    timestamp = str(int(timezone.now().timestamp()))  # Get current timestamp
    unique_code = (
        uuid.uuid4().hex[:8].upper()
    )  # Generate unique code and convert to uppercase

    return f"{timestamp}{unique_code}"


# Create your models here.
class Transaction(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )
    account = models.ForeignKey(
        "invest.Account",
        on_delete=models.CASCADE,
        related_name="transaction_account",
    )
    type = models.CharField(
        max_length=22,
        choices=TransactionType.choices,
        verbose_name="Transaction",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    paid = models.GeneratedField(
        expression=models.F("amount") - models.F("discount"),
        output_field=models.DecimalField(max_digits=15, decimal_places=2, default=0.00),
        db_persist=True,
    )
    verified = models.BooleanField(default=False)
    is_payment_success = models.BooleanField(default=False)
    receipt_number = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    payment_phone = models.CharField(max_length=255, blank=True)
    mpesa_transaction_code = models.CharField(max_length=1000, blank=True)
    payment_phone_number = models.CharField(max_length=1000, blank=True)
    currency = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    objects = TransactionQuerySet

    class Meta:
        get_latest_by = ["created_at"]

    def __str__(self):
        return f"{self.type} Transaction"

    def save(self, *args, **kwargs):
        self.receipt_number = generate_receipt_number()
        return super().save(*args, **kwargs)

    @property
    def invitor(self):
        return self.profile.referred_by

    @property
    def _paid(self):
        return self.paid

    @cached_property
    def __current_month_transaction(self):
        return self.account.transactions.filter(
            created_at__year=timezone.now().year,
            created_at__month=timezone.now().month,
        )

    def plan_transaction(self) -> Plan:

        subquery = (
            Plan.objects.filter(
                account=OuterRef("account"),
            )
            .order_by("created_at")
            .values("id")[:1]
        )

        return Transaction.objects.annotate(
            first_plan_id=Subquery(subquery),
        ).filter(account=self.account)


    def verify_transaction(self):
        """
        Verifies the transaction and updates the account balance based on the
        transaction type.
        """
        self.verified = True
        self.is_payment_success = True
        # Update account balance based on transaction type
        if self.type == "DEPOSIT":
            self._deposit_to_account()
        elif self.type == "WITHDRAWAL":
            self._withdraw_from_account()
        else:
            msg = f"Unsupported transaction type: {self.type}"
            raise ValueError(msg)
        self.save()


    def _deposit_to_account(self):
        """Handles balance update for deposit transactions."""
        self.account.balance += self.paid
        self.account.save()


    def _withdraw_from_account(self):
        """Handles balance update for withdrawal transactions, with balance check."""
        if self.account.balance < self.paid:
            msg = "Insufficient balance for withdrawal."
            raise ValueError(msg)
        self.account.balance -= self.paid
        self.account.save()


class PaymentMethod(models.Model):
    channel = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.channel}"


class AccountDeposit(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    account = models.ForeignKey(
        "invest.Account",
        on_delete=models.CASCADE,
        related_name="account_account_deposit",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    paid_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(max_length=500, default="To access more features")

    def __str__(self):
        return f"{self.profile.first_name} Account Topup"
