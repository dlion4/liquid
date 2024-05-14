from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from amiribd.users.models import User, Profile


class Position(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Position")
        verbose_name_plural = _("Positions")


class Agent(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="profile_agent"
    )
    position = models.OneToOneField(
        Position, on_delete=models.CASCADE, related_name="agent_position"
    )
    plantform = models.ManyToManyField(
        "Plantform",
        related_name="plantforms",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.profile.user.get_full_name()}"

    class Meta:
        verbose_name = _("Agent")
        verbose_name_plural = _("Agents")


class PlantformType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("PlantformType")
        verbose_name_plural = _("PlantformTypes")


class Plantform(models.Model):
    plantform_type = models.ForeignKey(
        PlantformType, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f"{self.plantform_type}"
