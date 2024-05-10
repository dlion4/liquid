from django.db import models
from django.utils.translation import gettext_lazy as _
from amiribd.users.models import User
import uuid
from datetime import timedelta
from django.utils import timezone


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
        super(Token, self).save(*args, **kwargs)
