from django.db import models
from amiribd.invest.models import Account, Plan
from .types import TransactionType
import uuid
from django.utils import timezone
from amiribd.users.models import Profile
from django.utils.functional import cached_property
from django.db.models import OuterRef, Subquery
from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Coalesce


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
    is_payment_success = models.BooleanField(default=False)
    receipt_number = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    payment_phone = models.CharField(max_length=255, blank=True, null=True)
    mpesa_transaction_code = models.CharField(max_length=1000, blank=True, null=True)
    payment_phone_number = models.CharField(max_length=1000, blank=True, null=True)
    currency = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

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





    def plan_transaction(self) -> Plan:
        """
        Get the first plan related to the account in the transaction.

        To bypass errors due to nested queries, we use the OuterRef and Coalesce functions to work around this error.

        Returns the plan associated with the account of this transaction.
        """
        # Subquery to find the account related to this transaction
        # account_subquery = Account.objects.filter(
        #     pk=OuterRef('account_id'),
        #     pool__profile=OuterRef('profile_id')
        # ).values('id')[:1]

        # # Subquery to find the first plan related to the account
        # plan_subquery = Plan.objects.filter(
        #     account=Subquery(account_subquery)
        # ).values('id')[:1]

        # # Fetch the plan using the subquery
        # plan = Plan.objects.filter(id=Subquery(plan_subquery)).first()

        # return plan
            # Subquery to find the first plan related to the account
        subquery = Plan.objects.filter(account=OuterRef('account')).order_by('created_at').values('id')[:1]
        
        transactions = Transaction.objects.annotate(
            first_plan_id=Subquery(subquery)
        ).filter(account=self.account)

        return transactions


class PaymentMethod(models.Model):
    channel = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.channel}"
