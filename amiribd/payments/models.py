from django.db import models
from amiribd.transactions.models import PaymentMethod
from amiribd.users.models import Profile


# Create your models here.
class Payment(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="my_payment_channel"
    )
    channel = models.ForeignKey(
        PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True
    )
    account = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.channel} - {self.account}"


class PaystackPaymentStatus(models.Model):
    email = models.EmailField(max_length=100)
    status = models.CharField(max_length=100)
    reference = models.CharField(max_length=1000)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {self.status} - {self.reference}"
