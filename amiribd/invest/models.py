from django.db import models
from amiribd.users.models import Profile
from .types import (
    PoolTypeObjects,
    AccountTypeObjects,
    PlanTypeObjects,
    PlanStatus,
    AccountTypeObjects,
)
from django.db.models import Sum
from django.urls import reverse
from django.utils.text import slugify
from django.utils.termcolors import colorize
from datetime import timedelta
from django.utils import timezone
from django.utils.functional import cached_property
from decimal import Decimal
from django.db.models import F, OuterRef, Q, Subquery, DecimalField
from django.db.models.functions import Coalesce
from django_extensions.db.fields import AutoSlugField


class PoolType(models.Model):
    type = models.CharField(
        max_length=10,
        choices=PoolTypeObjects.choices,
        default=PoolTypeObjects.INDIVIDUAL,
        unique=True,
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
        return f"{self.type}"

    @property
    def owner(self):
        return self.profile.user

    @property
    def account(self):
        return self.account_pool.type


class PoolFeature(models.Model):
    pool = models.OneToOneField(
        Pool, on_delete=models.CASCADE, related_name="pool_feature"
    )
    feature = models.TextField(blank=True, null=True)


class AccountType(models.Model):
    type = models.CharField(
        max_length=10,
        choices=(("Basic", "Basic"), ("Standard", "Standard")),
        default="Basic",
    )
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.type}"


class Account(models.Model):
    pool = models.OneToOneField(
        Pool, on_delete=models.CASCADE, related_name="account_pool"
    )
    type = models.ForeignKey(
        AccountType,
        on_delete=models.CASCADE,
        related_name="account_type",
        verbose_name="account_type",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    # interest = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    @property
    def account_owner(self):
        return self.pool.profile.user

    @property
    def invite_profit(self):
        __invite_profit = sum(
            amount.paid
            for amount in self.transaction_account.all().filter(
                source__icontains="Referral Earnings"
            )
        )

        print("Invite Profit: ", __invite_profit)
        return Decimal("0.00") if None else __invite_profit

    @property
    def obtain_total_investment(self):
        total = Decimal(
            self.transaction_account.filter(
                Q(account__pool__profile=self.pool.profile)
                & Q(source="Account Registration")
            ).aggregate(total=Sum("paid"))["total"]
        )

        return total if total is not None else Decimal("0.0")

    @property
    def withdrawable_investment(self):
        return self.balance - self.obtain_total_investment

    @property
    def latest_invite_interest(self):
        __latest_invite_interest = (
            self.transaction_account.filter(
                Q(account__pool__profile=self.pool.profile)
                & Q(source__icontains="Referral Earnings")
            )
            .latest()
            .paid
        )

        print(colorize("Latest Interest: ", fg="white"), __latest_invite_interest)
        return Decimal("0.00") if None else __latest_invite_interest

    @cached_property
    def percentage_profit(self):
        return round((self.latest_invite_interest / self.invite_profit) * 100, 1)

    def __str__(self):
        return self.type.type


class PlanType(models.Model):
    type = models.CharField(
        max_length=15, choices=PlanTypeObjects.choices, default=PlanTypeObjects.BRONZE
    )
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    percentage_return = models.FloatField(default=0)

    def __str__(self):
        return f"{self.type}"


class Plan(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="account_plan"
    )
    type = models.ForeignKey(
        PlanType,
        on_delete=models.CASCADE,
        related_name="plan_type",
        verbose_name="Plan",
    )
    slug = AutoSlugField(populate_from="type", unique=False)
    min_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    max_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    # Use GeneratedField for the fee column
    fee = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, choices=PlanStatus.choices, default=PlanStatus.RUNNING
    )
    payment_method = models.CharField(max_length=100, blank=True, null=True)

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

    @property
    def plan_profile(self):
        return self.account.pool.profile

    @property
    def percentage_return(self):
        return self.type.percentage_return

    @property
    def interest_return(self):
        amount = round(self.account.balance * Decimal(self.percentage_return) / 100, 2)
        print("Interest Return: ", amount)
        return amount

    def get_absolute_url(self):
        return reverse(
            "dashboard:invest:plan",
            kwargs={"plan_slug": self.slug, "plan_id": self.pk},
        )
