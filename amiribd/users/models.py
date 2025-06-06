from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import CharField
from django.db.models import EmailField
from django.db.models import QuerySet
from django.db.models import Value
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

# from .actions import generate_referral_code
from .utils import generate_referral_code


class ConcatField(models.Func):
    arg_joiner = " || "
    function = None
    output_field = models.TextField()
    template = "%(expressions)s"


class User(AbstractUser):
    """
    Default custom user model for amiribd.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    email = EmailField(_("email address"), unique=True)
    username = CharField(
        _("username"), max_length=255, unique=False, blank=True,
    )
    verified = models.BooleanField(default=False)
    status = models.CharField(
        max_length=255,
        default="PENDING",
        choices=(
            ("PENDING", "pending"),
            ("COMPLETED", "completed"),
            ("BLOCKED", "blocked"),
            ("SUSPENDED", "suspended"),
        ),
    )
    date_joined = models.DateField(auto_now_add=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"pk": self.id})

    @cached_property
    def referrals_count(self):
        return self.referrals().count()

    def referrals(self) -> QuerySet["Profile"]:
        return self.profile_referred_by.all()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split("@")[0]
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile_user",
    )
    first_name = models.CharField(blank=True, max_length=100)
    last_name = models.CharField(blank=True, max_length=100)
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    full_name = models.GeneratedField(
        expression=ConcatField(
            "first_name",
            Value(" "),
            "last_name",
        ),
        output_field=models.TextField(),
        db_persist=True,
    )
    kyc_completed = models.BooleanField(default=False)
    kyc_validated = models.BooleanField(default=False)
    kyc_completed_at = models.DateTimeField(null=True, blank=True)
    is_address_set = models.BooleanField(default=False)
    is_document_set = models.BooleanField(default=False)
    phone_regex = RegexValidator(
        regex=r"^[0-9]\d{8,14}$",
        message="Phone number must start with a digit and be 9 to 15 digits in total.",
    )
    phone_number = models.CharField(
        max_length=20, blank=True, validators=[phone_regex],
    )
    date_of_birth = models.DateField(null=True, blank=True)
    initials = models.CharField(max_length=2, blank=True, default="AB")
    referral_code = models.CharField(max_length=200, blank=True)
    referred_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="profile_referred_by",
    )
    job_applications = models.ManyToManyField(
        "jobs.Job",
        blank=True,
        related_name="profile_job_applications",
    )
    plans = models.ManyToManyField("invest.Plan", blank=True)
    adverts = models.ManyToManyField("adverts.Advert", blank=True)
    accepted_job_applications = models.ManyToManyField(
        "jobs.JobApplication",
        blank=True,
        related_name="profile_accepted_job_applications",
    )
    is_subscribed = models.BooleanField(default=False)
    is_waiting_plan_verification = models.BooleanField(default=False)
    subscription_level = models.CharField(
        max_length=20,
        choices=(
            ("BASIC", "Basic"),
            ("PREMIUM", "Premium"),
            ("VIP", "VIP"),
        ),
        default="BASIC",
    )
    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.initials = self.generate_initials()

    def generate_initials(self) -> str | None:
        """
        Use the full name that has been generated to get the initial
        """
        if self.full_name:
            names = self.full_name.split()
            initials = [name[0].upper() for name in names]
            return "".join(initials[:2])
        return self.initials

    @cached_property
    def referrals(self) -> int:
        return self.user.referrals_count

    def get_referral_signup_url(self):
        return reverse("users:referred-signup", kwargs={
            "referral_code":self.referral_code,
        })




    @property
    def profile_identity(self):
        if self.full_name:
            return self.full_name.title()
        return self.user.email[: self.user.email.index("@")].title()

    # for websocket url generation
    @property
    def get_ws_sender_url(self):
        return f"@{self.user.username}".lower()

    # same as above
    @property
    def get_ws_receiver_url(self):
        return f"@{self.user.username}"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.referral_code = generate_referral_code(profile.user.pk)
        profile.save()


class Address(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="profile_address",
    )
    addr_line1 = models.CharField(max_length=255)
    addr_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.profile.user.username} Address"


class DocumentType(models.TextChoices):
    NI = "NI", "National Id"
    PT = "PT", "Passport"
    DL = "DL", "Driving License"


def user_directory_path(instance, filename) -> str:
    # file will be uploaded to MEDIA_ROOT/profiles/kyc/<year>/<month>/<day>/<username>/<filename>  # noqa: E501

    return (
        f"profiles/kyc/{now().year}/{now().month}/{now().day}/{instance.profile.user.username}/{instance.profile.pk}/{filename}"
    )


class Document(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="profile_document",
    )
    document_type = models.CharField(max_length=2, default=DocumentType.NI)
    document = models.ImageField(upload_to=user_directory_path)
    read_terms = models.BooleanField(default=False)
    correct_information = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.profile.user.username} Verification Document"
# The `ValidatedEmailAddress` class represents a model in Django with fields for email address and
# creation timestamp.

class ValidatedEmailAddress(models.Model):
    email_address = models.EmailField(unique=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Validated Email Address"
        verbose_name_plural = "Validated Email Address"

    def __str__(self):
        return self.email_address
