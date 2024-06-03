from django.db import models


class PoolTypeObjects(models.TextChoices):
    INDIVIDUAL = "INDIVIDUAL", "Individual"
    FAMILY = "FAMILY", "Family"
    JOINT = "JOINT", "Joint"
    INSTITUTON = "INSTITUTON", "Instituton"


class AccountTypeObjects(models.TextChoices):
    BASIC = "BASIC", "Basic"
    STANDARD = "STANDARD", "Standard"


class PlanTypeObjects(models.TextChoices):
    BRONZE = "BRONZE", "  Bronze"
    SILVER = "SILVER", "  Silver"
    DIAMOND = "DIAMOND", "  Diamond"


class PlanStatus(models.TextChoices):
    RUNNING = "RUNNING", "Running"
    STOPPED = "STOPPED", "Stopped"
    CANCELLED = "CANCELLED", "Cancelled"
