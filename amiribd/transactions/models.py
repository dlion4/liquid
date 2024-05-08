from django.db import models
from amiribd.invest.models import Account
from .types import TransactionType
import uuid
from django.utils import timezone
from amiribd.users.models import Profile
from django.utils.functional import cached_property


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
        Account, on_delete=models.CASCADE, related_name="transaction_account"
    )
    type = models.CharField(
        max_length=22, choices=TransactionType.choices, verbose_name="Transaction"
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
    receipt_number = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.type} Transaction"

    @property
    def invitor(self):
        self.profile.referred_by

    @property
    def _paid(self):
        return self.paid

    # @cached_property
    # def __current_month_transaction(self):
    #     return self.account.transactions.filter(
    #         created_at__year=timezone.now().year,
    #         created_at__month=timezone.now().month,
    #     )

    class Meta:
        get_latest_by = ["created_at"]

    def save(self, *args, **kwargs):
        self.receipt_number = generate_receipt_number()
        super().save(*args, **kwargs)


class PaymentMethod(models.Model):
    channel = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.channel}"
