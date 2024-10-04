import uuid
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _

from amiribd.users.models import User


class SingletonModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # Prevent deletion

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


# Create your models here.
class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4(), editable=False)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.token)

    def save(self, *args, **kwargs):
        if not self.expires:
            self.expires = timezone.now() + timedelta(hours=1)
        super().save(*args, **kwargs)


class AuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField()
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.code)


class SecretCredential(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="name that will be used in the environment variable")
    email = models.EmailField(max_length=100, blank=True)
    project_id = models.UUIDField(blank=True, null=True, max_length=3000)
    secret_key = models.CharField(max_length=1000, blank=True)
    client_id = models.CharField(max_length=1000, blank=True)
    api_key = models.CharField(max_length=3000)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # other fields...

    class Meta:
        verbose_name = "Secret Credential"
        verbose_name_plural = "Secret Credentials"

    def __str__(self):
        return str(self.name)

    @property
    def timesince(self):
        return f"{timesince(self.created_at, timezone.now())} ago"




class Secret(models.Model):
    source = models.ForeignKey(
        SecretCredential, on_delete=models.CASCADE,
        related_name="secret_credentials_source", blank=True, null=True)
    name = models.CharField(max_length=100, blank=True)
    value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "name"],
                name="unique_secret_source_name",
            ),
        ]
    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.source.is_active:
            self.is_active=True
        else:
            self.is_active = False
        if self.name is None:
            self.name = self.source.name
        super().save(*args,**kwargs)
