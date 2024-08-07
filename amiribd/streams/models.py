import json
from django.db import models
# from .serializers import PostSerializer
from django.urls import reverse
from django.utils.text import slugify
from amiribd.users.models import Profile
from amiribd import redis_client, notification_websocket_client
from asgiref.sync import sync_to_async, async_to_sync
# Create your models here.
class Room(models.Model):

    class RoomTheme(models.TextChoices):
        P = "P", "primary"
        S = "S", "secondary"
        D = "D", "default"
        L = "L", "light"
        I = "I", "info"
        W = "W", "warning"

    class RoomType(models.TextChoices):
        Pb = "Pb", "public"
        P = "P", "private"
        T = "T", "Temporary"

    owner = models.ForeignKey(
        Profile,
        verbose_name="owner",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="room_owner",
    )
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, max_length=255)
    icon = models.CharField(max_length=255, default="fi-ts-customer-service")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    theme = models.CharField(
        max_length=1, choices=RoomTheme.choices, default=RoomTheme.P
    )
    type = models.CharField(max_length=2, choices=RoomType.choices, default=RoomType.Pb)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("dashboard:streams:room-detail", kwargs={"room_slug": self.slug})

    @property
    def kind(self):
        return self.get_type_display()


class RoomMessage(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="room_messages"
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="room_messages"
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.room.name} message"


class Favorite(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="favorites"
    )
    rooms = models.ManyToManyField(
        Room,
    )


class Message(models.Model):
    sender = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="message_sender",
    )
    receiver = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="message_receiver",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender.user.username} to {self.receiver.user.username}"

    def get_absolute_url(self):
        return reverse(
            "dashboard:streams:message-detail",
            kwargs={"pk": self.pk, "receiver": self.receiver.get_ws_sender_url},
        )

    class Meta:
        get_latest_by = "created_at"


class InboxAbstract(models.Model):

    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seen = models.BooleanField(default=False)

    class Meta:
        get_latest_by = "created_at"
        abstract = True


class Inbox(InboxAbstract):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="inbox_message"
    )


class AdminInbox(InboxAbstract):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="admin_inbox_message"
    )


class Archive(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="archived_messages"
    )
    archiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="archiver_messages"
    )
    archived_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archived Message Id {self.message.pk}"


class Notification(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):

        # # Push notification to the sender's WebSocket connection
        # redis_client.publish(
        #     self.sender.get_ws_sender_url,
        #     {
        #         "type": "notification",
        #         "title": self.title,
        #     },
        # )
        super(Notification, self).save(*args, **kwargs)
        redis_client.upload_instance_to_redis(
            instance_name="notification",
            instance_id=self.pk,
            instance_data={"title": self.title},
            expiry=600  # 10 minutes
        )

        notification_websocket_client.send_notification(
            notification_group="notifications_group", 
            message='', 
            redis_instance_id=self.pk,
            redis_instance_name='notification'
        )



class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True, related_name="profile_update")
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # # Publish the post data to the Redis channel
        # redis_client.upload_instance_to_redis(
        #     instance_name="posts",
        #     instance_id=self.pk,
        #     instance_data=PostSerializer(instance=self).data,
        #     expiry=600  # 10 minutes
        # )

        # notification_websocket_client.send_notification(
        #     notification_group="posts_group", 
        #     message='', 
        #     redis_instance_id=self.pk,
        #     redis_instance_name='posts'
        # )
    


