from django.db import models
from amiribd.users.models import Profile
from .types import PoolType, AccountType, PlanType, PlanStatus, TransactionType

from django.db.models import OuterRef, Subquery, DecimalField
from django.db.models.functions import Coalesce


# Create your models here.
class Pool(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="account_profile"
    )
    type = models.CharField(
        max_length=25, default=PoolType.INDIVIDUAL, choices=PoolType.choices
    )
    fee = models.DecimalField(max_digits=15, decimal_places=2, default=300.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type} Pool"


class PoolFeature(models.Model):
    pool = models.OneToOneField(
        Pool, on_delete=models.CASCADE, related_name="pool_feature"
    )
    feature = models.TextField(blank=True, null=True)


class Account(models.Model):
    pool = models.ForeignKey(
        Pool, on_delete=models.CASCADE, related_name="account_pool"
    )
    type = models.CharField(
        max_length=10, choices=AccountType.choices, default=AccountType.BASIC
    )
    fee = models.DecimalField(max_digits=15, decimal_places=2, default=300.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=300.00)

    def __str__(self):
        return f"{self.type} Account"


class Plan(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="account_plan"
    )
    plan = models.CharField(
        max_length=15, choices=PlanType.choices, default=PlanType.BRONZE
    )
    min_amount = models.DecimalField(max_digits=15, decimal_places=2, default=300.00)
    max_amount = models.DecimalField(max_digits=15, decimal_places=2, default=300.00)
    # Use GeneratedField for the fee column
    fee = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    percentage_return = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, choices=PlanStatus.choices, default=PlanStatus.RUNNING
    )

    def __str__(self):
        return f"{self.plan} Plan"

    def save(self, *args, **kwargs):
        # Override save method to set the GeneratedField value
        self.fee = self._calculate_fee()
        super().save(*args, **kwargs)

    def _calculate_fee(self):
        # Subquery to fetch related Account's fee
        account_fee_subquery = Account.objects.filter(pk=OuterRef("account_id")).values(
            "fee"
        )[:1]
        # Use Coalesce to handle cases where account_fee_subquery returns None
        return Coalesce(Subquery(account_fee_subquery), 0)


class Transaction(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transaction_account"
    )
    type = models.CharField(max_length=22, choices=TransactionType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    verified = models.BooleanField(default=False)
    receipt_number = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.type} Transaction"
