from django.db import models
from amiribd.users.models import Profile
from .types import (
    PoolTypeObjects,
    AccountTypeObjects,
    PlanTypeObjects,
    PlanStatus,
    AccountTypeObjects,
)

from django.db.models import OuterRef, Subquery, DecimalField
from django.db.models.functions import Coalesce


class PoolType(models.Model):
    type = models.CharField(
        max_length=10,
        choices=PoolTypeObjects.choices,
        default=PoolTypeObjects.INDIVIDUAL,
    )
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.type} Pool"


# Create your models here.
class Pool(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="pool_account_profile"
    )
    type = models.ForeignKey(
        PoolType,
        on_delete=models.CASCADE,
        related_name="pool_type",
        verbose_name="pool_type",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type} Pool"


class PoolFeature(models.Model):
    pool = models.OneToOneField(
        Pool, on_delete=models.CASCADE, related_name="pool_feature"
    )
    feature = models.TextField(blank=True, null=True)


class AccountType(models.Model):
    type = models.CharField(
        max_length=10,
        choices=AccountTypeObjects.choices,
        default=AccountTypeObjects.BASIC,
    )
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.type} Account"


class Account(models.Model):
    pool = models.ForeignKey(
        Pool, on_delete=models.CASCADE, related_name="account_pool"
    )
    type = models.ForeignKey(
        AccountType, on_delete=models.CASCADE, related_name="account_type"
    )
    fee = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.type} Account"


class PlanType(models.Model):
    type = models.CharField(
        max_length=15, choices=PlanTypeObjects.choices, default=PlanTypeObjects.BRONZE
    )
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.type} Plan"


class Plan(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="account_plan"
    )
    type = models.ForeignKey(
        PlanType, on_delete=models.CASCADE, related_name="plan_type"
    )
    min_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    max_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    # Use GeneratedField for the fee column
    fee = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    percentage_return = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, choices=PlanStatus.choices, default=PlanStatus.RUNNING
    )

    def __str__(self):
        return f"{self.type} Plan"

    # def save(self, *args, **kwargs):
    #     # Override save method to set the GeneratedField value
    #     self.fee = self._calculate_fee()
    #     super().save(*args, **kwargs)

    def _calculate_fee(self):
        # Subquery to fetch related Account's fee
        account_fee_subquery = Account.objects.filter(pk=OuterRef("account_id")).values(
            "fee"
        )[:1]
        # Use Coalesce to handle cases where account_fee_subquery returns None
        return Coalesce(Subquery(account_fee_subquery), 0)
