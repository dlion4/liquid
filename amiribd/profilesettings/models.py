from django.db import models

from amiribd.users.models import Profile

# Create your models here.


class Notification(models.Model):
    title = models.CharField(max_length=255, unique=True, help_text="News")
    description = models.CharField(
        max_length=255,
        help_text="News",
        default="You will get only those email notification what you want.",
    )

    def get_notification_types(self):
        return self.notification_types.all()

    def __str__(self):
        return self.title


class NotificationType(models.Model):
    notification = models.ForeignKey(
        Notification,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notification_types",
    )
    profile = models.ManyToManyField(
        Profile, related_name="profile_notifications", blank=True
    )
    label = models.CharField(max_length=255, blank=True, null=True)
    notify = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.notification} - {self.label}"


class NotificationSubscription(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="notification_profile_subscription",
    )
    notify_label_type = models.OneToOneField(
        NotificationType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notify_label_type",
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.profile.user.username} - {self.notify_label_type.label}"
