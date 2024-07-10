from django.db import models
from amiribd.users.models import Profile
from .types import (
    PoolTypeObjects,
    AccountTypeObjects,
    PlanTypeObjects,
    PlanStatus,
    AccountTypeObjects,
)
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.core.validators import RegexValidator
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
import random
import string


def generate_ssid(instance, k=10):

    char = "".join(
        random.choices(
            str(
                str(instance.pk)
                + str(instance.pool.profile.pk)
                + string.ascii_uppercase
                + string.digits
            ),
            k=k,
        )
    )

    return char


class PoolType(models.Model):
    type = models.CharField(
        max_length=10,
        choices=PoolTypeObjects.choices,
        default=PoolTypeObjects.INDIVIDUAL,
        unique=True,
    )
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.type}"


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

    class Meta:
        verbose_name = _("Pool")
        verbose_name_plural = _("Pools")


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
    account_ssid = models.CharField(max_length=200, blank=True, null=True)


    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

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

        return Decimal("0.00") if None else __invite_profit

    @property
    def obtain_total_investment(self):
        total = Decimal(
            self.transaction_account.filter(
                Q(account__pool__profile=self.pool.profile)
                & Q(source="Account Registration")
            ).aggregate(total=Sum("paid"))["total"]
        )

        if total:
            return total
        return Decimal("0.00")

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

        return Decimal("0.00") if None else __latest_invite_interest

    @cached_property
    def percentage_profit(self):
        return round((self.latest_invite_interest / self.invite_profit) * 100, 1)

    def __str__(self):
        return f"{self.pool.profile.profile_identity} ~ {self.account_ssid}"

    def save(self, *args, **kwargs):
        if not self.account_ssid:
            self.account_ssid = generate_ssid(self, 18)
        super().save(*args, **kwargs)


class PlanType(models.Model):
    type = models.CharField(
        max_length=15, choices=PlanTypeObjects.choices, default=PlanTypeObjects.BRONZE
    )
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    percentage_return = models.FloatField(default=0)
    icon = models.CharField(max_length=100, blank=True, null=True)
    svg = models.FileField(upload_to="icons/", blank=True, null=True)
    interval = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Interval ie Monthly, Yearly, Unlimited",
        default="Unlimited",
    )
    description = models.CharField(
        blank=True,
        null=True,
        help_text="Description",
        max_length=500,
        default="Unlimited access with priority support, 99.95% uptime, powerfull features and more...",
    )
    theme = models.CharField(max_length=100, default="orange",choices=(
        ("primary", "primary"),
        ("secondary", "secondary"),
        ("danger", "danger"),
        ("info", "info"),
        ("success", "success"),
        ("orange", "orange"),
        ("teal", "teal"),
        ("pink", "pink"),
        ("azure", "azure"),
    ))

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
    sku = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    mpesa_transaction_code = models.CharField(max_length=1000, blank=True, null=True)
    payment_phone_number = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"{self.type} Plan"

    def _generate_sku(self):
        import random

        random_part = "".join(
            [str(random.randint(0, 9)) for _ in range(7)]
        )  # Generate 7 random digits
        return f"{self.pk}{random_part}"  # Combine PK and random digits to form an 8-character SKU

    def save(self, *args, **kwargs):
        if self.sku is None:
            self.sku = self._generate_sku()
        super().save(*args, **kwargs)

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
        return round(self.account.balance * Decimal(self.percentage_return) / 100, 2)

    def get_absolute_url(self):
        return reverse(
            "subscriptions:subscription",
            kwargs={"plan_slug": self.slug, "plan_id": self.pk},
        )

    class Meta:
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=["account", "type"], name="unique_account_plan_type"
        #     )
        # ]
        get_latest_by = ["created_at"]
        pass


class AccountWithdrawalAction(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="account_event_action"
    )
    action = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=(
            ("Withdrawal", "Withdrawal"),
            ("Deposit", "Deposit"),
        ),
        default="Withdrawal",
    )
    status = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=(
            ("Initiated", "Initiated"),
            ("Resolved", "Resolved"),
            ("Cancelled", "Cancelled"),
        ),
        default="Initiated",
    )
    withdrawal_date = models.DateField(blank=True, null=True)
    withdrawal_time = models.TimeField(blank=True, null=True)
    amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    channel = models.ForeignKey(
        "transactions.PaymentMethod",
        related_name="payment_channel_account_event",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    phone_regex = RegexValidator(
        regex=r"^[0-9]\d{8,14}$",
        message="Phone number must start with a digit and be 9 to 15 digits in total.",
    )
    payment_phone_number = models.CharField(
        max_length=20, null=True, blank=True, validators=[phone_regex]
    )
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.account} - {self.action} - {self.status}"


class AccountEventDeposit(models.Model):
    pass
