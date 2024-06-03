from django.db import models

# Create your models here.
from django.utils.timezone import now
from amiribd.users.models import Profile
from decimal import Decimal


class EarningScheme(models.Model):
    views = models.PositiveBigIntegerField(
        default=0,
        help_text="Total number of views",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(auto_now=True)
    rejected = models.BooleanField(default=False)
    rejected_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def file_user_directory_path(instance, filename) -> str:
    # file will be uploaded to MEDIA_ROOT/profiles/kyc/<year>/<month>/<day>/<username>/<filename>

    return "profiles/whatsapp/{0}/{1}/{2}/{3}/{4}".format(
        now().year,
        now().month,
        now().day,
        instance.profile.pk,
        filename,
    )


class WhatsAppEarningScheme(EarningScheme):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )
    file = models.FileField(upload_to=file_user_directory_path)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)

    @property
    def amount(self):
        return Decimal(self.views) * self.price

    def __str__(self):
        return str(self.profile.user.username)
