from typing import ClassVar
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Value
from .managers import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from django.utils.timezone import now


class ConcatFiels(models.Func):
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
        _("username"), max_length=255, unique=False, blank=True, null=True
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

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split("@")[0]
        super(User, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile_user"
    )
    first_name = models.CharField(blank=True, null=True, max_length=100)
    last_name = models.CharField(blank=True, null=True, max_length=100)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    full_name = models.GeneratedField(
        expression=ConcatFiels(
            "first_name",
            Value(" "),
            "last_name",
        ),
        output_field=models.TextField(),
        db_persist=True,
    )
    kyc_completed = models.BooleanField(default=False)
    kyc_completed_at = models.DateTimeField(null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r"^[0-9]\d{8,14}$",
        message="Phone number must start with a digit and be 9 to 15 digits in total.",
    )
    phone_number = models.CharField(
        max_length=20, null=True, blank=True, validators=[phone_regex]
    )
    date_of_birth = models.CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile_user.save()


class Address(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="profile_address"
    )
    addr_line1 = models.CharField(max_length=255)
    addr_line2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.profile.user.username} Address"


class DocumentType(models.TextChoices):
    NI = "NI", "National Id"
    PT = "PT", "Passport"
    DL = "DL", "Driving Licence"


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profiles/kyc/<year>/<month>/<day>/<username>/<filename>

    return "profiles/kyc/{0}/{1}/{2}/{3}/{4}/{5}".format(
        now().year,
        now().month,
        now().day,
        instance.profile.user.username,
        instance.profile.pk,
        filename,
    )


class Document(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="profile_document"
    )
    document_type = models.CharField(max_length=2, default=DocumentType.NI)
    document = models.ImageField(upload_to=user_directory_path)
    read_terms = models.BooleanField(default=False)
    correct_information = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.profile.user.username} Verification Document"
