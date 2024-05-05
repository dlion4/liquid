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

    def __str__(self):
        return f"{self.user.username} Profile"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile_user.save()
