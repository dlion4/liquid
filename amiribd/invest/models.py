import contextlib
import random
import string
from datetime import date
from datetime import timedelta
from decimal import Decimal

from django.core.validators import RegexValidator
from django.db import models
from django.db.models import F
from django.db.models import OuterRef
from django.db.models import Q
from django.db.models import Subquery
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from amiribd.users.models import Profile

from .types import PlanStatus
from .types import PlanTypeObjects
from .types import PoolTypeObjects


def generate_ssid(instance, k=10):

    return "".join(
        random.choices(
            str(
                str(instance.pk)
                + str(instance.pool.profile.pk)
                + string.ascii_uppercase
                + string.digits,
            ),
            k=k,
        ),
    )


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
        Profile, on_delete=models.CASCADE, related_name="pool_account_profile",
    )
    type = models.ForeignKey(
        PoolType,
        on_delete=models.CASCADE,
        related_name="pool_type",
        verbose_name="pool_type",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = _("Pool")
        verbose_name_plural = _("Pools")

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
        Pool, on_delete=models.CASCADE, related_name="pool_feature",
    )
    feature = models.TextField(blank=True)

    def __str__(self):
        return str(self.pool.type.type)


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
        Pool, on_delete=models.CASCADE, related_name="account_pool",
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
    # interest = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # noqa: E501, ERA001
    account_ssid = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        get_latest_by = "updated_at"

    def __str__(self):
        return f"{self.pool.profile.profile_identity} ~ {self.account_ssid}"

    def save(self, *args, **kwargs):
        if not self.account_ssid:
            self.account_ssid = generate_ssid(self, 18)
        super().save(*args, **kwargs)

    @cached_property
    def locked_balance_account(self):
        return self.obtain_total_investment


    @property
    def account_owner(self):
        return self.pool.profile.user

    @property
    def invite_profit(self):
        __invite_profit = sum(
            amount.paid
            for amount in self.transaction_account.all().filter(
                source__icontains="Referral Earnings",
            )
        )

        return Decimal("0.00") if None else __invite_profit

    @property
    def obtain_total_investment(self):
        total_investment = (
            self.transaction_account.filter(
                account__pool__profile=self.pool.profile,
                source="Account Registration",
            )
            .aggregate(total=Sum("paid"))
            .get("total", 0.00)
        )
        return Decimal(total_investment or "0.00")

    @property
    def withdrawable_investment(self):
        return self.balance - self.obtain_total_investment

    @property
    def latest_invite_interest(self):
        __latest_invite_interest = (
            self.transaction_account.filter(
                Q(account__pool__profile=self.pool.profile)
                & Q(source__icontains="Referral Earnings"),
            )
            .latest()
            .paid
        )

        return Decimal("0.00") if None else __latest_invite_interest

    @cached_property
    def percentage_profit(self):
        return round((self.latest_invite_interest / self.invite_profit) * 100, 1)


class PlanType(models.Model):
    type = models.CharField(
        max_length=15, choices=PlanTypeObjects.choices, default=PlanTypeObjects.BRONZE,
    )
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    percentage_return = models.FloatField(default=0)
    icon = models.CharField(max_length=100, blank=True, default="")
    svg = models.FileField(upload_to="icons/", blank=True, null=True)
    interval = models.CharField(
        max_length=100,
        blank=True,
        help_text="Interval ie Monthly, Yearly, Unlimited",
        default="Unlimited",
    )
    description = models.CharField(
        blank=True,
        help_text="Description",
        max_length=500,
        default="Unlimited access with priority support, 99.95% uptime, powerful features and more...",  # noqa: E501
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
        Account, on_delete=models.CASCADE, related_name="account_plan",
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
        max_length=20, choices=PlanStatus.choices, default=PlanStatus.RUNNING,
    )
    payment_method = models.CharField(max_length=100, blank=True, default="MPESA")
    sku = models.CharField(max_length=100, blank=True)
    is_paid = models.BooleanField(default=False)
    mpesa_transaction_code = models.CharField(max_length=1000, blank=True)
    payment_phone_number = models.CharField(max_length=1000, blank=True)

    class Meta:
        get_latest_by = ["created_at"]

    def __str__(self):
        return f"{self.type} Plan"

    def save(self, *args, **kwargs):
        if self.sku is None:
            self.sku = self._generate_sku()
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse(
            "subscriptions:subscription",
            kwargs={"plan_slug": self.slug, "plan_id": self.pk},
        )

    def _generate_sku(self):
        import random

        random_part = "".join(
            [str(random.randint(0, 9)) for _ in range(7)],  # noqa: S311
        )  # Generate 7 random digits
        # Combine PK and random digits to form an 8-character SKU
        return f"{self.pk}{random_part}"


    def _calculate_fee(self):
        # Subquery to fetch related Account's fee
        account_fee_subquery = Account.objects.filter(pk=OuterRef("account_id")).values(
            "fee",
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
    def plan_profile_email(self):
        return self.plan_profile.user.email

    @property
    def interest_return(self):
        return round(self.account.balance * Decimal(self.percentage_return) / 100, 2)


class AccountWithdrawalAction(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="account_event_action",
    )
    action = models.CharField(
        max_length=100,
        blank=True,
        choices=(
            ("Withdrawal", "Withdrawal"),
            ("Deposit", "Deposit"),
        ),
        default="Withdrawal",
    )
    status = models.CharField(
        max_length=100,
        blank=True,
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
        max_length=20, blank=True, validators=[phone_regex],
    )
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.account} - {self.action} - {self.status}"


class AccountEventDeposit(models.Model):
    def __str__(self):
        return ""

class SavingPlan(models.Model):
    title = models.CharField(max_length=100)
    interest = models.FloatField(default=1, help_text="The interest rate charged daily")
    term = models.IntegerField(
        default=1, help_text="Maturation term. Example value 3 days")
    principal = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00, help_text="Investment amount")
    description = models.CharField(
        max_length=300, blank=True,
        default="Choose your investment plan and start earning.")
    # amount = models.GeneratedField(  # noqa: ERA001 RUF100
    #     expression=models.ExpressionWrapper(  # noqa: ERA001 RUF100
    #         F("principal") +  (F("principal") * (1 + F("interest"))) * (F("term") / 7),  # noqa: E501, ERA001, RUF100
    #         output_field=models.DecimalField(  # noqa: ERA001 RUF100
    #             max_digits=15, decimal_places=2, default=0.00),
    #     ),
    #     output_field=models.DecimalField(max_digits=15, decimal_places=2, default=0.00),  # noqa: E501, ERA001, RUF100
    #     db_persist=True,  # noqa: ERA001
    # )  # noqa: ERA001, RUF100
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def amount(self):
        return f"{(self.principal + Decimal(self.earned_interest)):.2f}"


    @property
    def percentage_rate(self):
        return self.interest / 100

    @property
    def earned_interest(self):
        return (f"{(self.principal *Decimal(self.percentage_rate) *Decimal(self.term/7)):.2f}")

class SavingInvestmentPlan(models.Model):
    scheme = models.ForeignKey(
        SavingPlan, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(
        max_length=100,
        choices=(
            ("pending", "Pending"),
            ("approved", "approved"),
            ("declined", "declined"),
            ("expired", "expired"),
        ),
        default="pending",
    )

    def __str__(self):
        return self.scheme


class InvestMentSaving(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL,
        blank=True, null=True)
    principal_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    duration_of_saving_investment = models.CharField(max_length=300, blank=True)
    interest_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    expected_daily_interest_plus_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    instruction = models.TextField(blank=True,max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.profile} - {self.principal_amount}"
    def save(self, *args, **kwargs):
        self.interest_amount = Decimal(self.interest_amount) * Decimal(
            self.extract_days().days,
        )
        self.expected_daily_interest_plus_amount = (
            self.principal_amount + self.interest_amount,
        )
        super().save(*args, **kwargs)

    def extract_days(self):
        """
        Extract the number of days from the `duration_of_saving_investment` field.
        For example, if the duration is '2 weeks', this will return 14 days.
        """
        duration_parts = self.duration_of_saving_investment.split()
        if len(duration_parts) >= 2:
            number = int(duration_parts[0])  # Extracts the numerical part (e.g., 2)
            unit = duration_parts[
                1
            ].lower()  # Extracts the time unit (e.g., 'days' or 'weeks')

            if unit in ("days", "day"):
                return timedelta(days=number)
            if unit in ("weeks", "week"):
                return timedelta(weeks=number)
        return timedelta(0)  # Default to 0 days if invalid input

    def lock_end_date(self):
        """
        Calculate the end date when the investment will be unlocked.
        Adds the extracted days to the creation date.
        """
        duration_days = self.extract_days()
        return self.created_at + duration_days

    def can_withdraw(self):
        """
        Check if the investment can be withdrawn based on the current date.
        The amount is locked until the lock_end_date.
        """
        return date.today() >= self.lock_end_date()  # noqa: DTZ011

    @property
    def earned_interest(self):
        return self.principal_amount * Decimal("2.00")
