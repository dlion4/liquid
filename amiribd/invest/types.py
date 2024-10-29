from django.db import models


class PoolTypeObjects(models.TextChoices):
    INDIVIDUAL = "INDIVIDUAL", "Individual"
    FREELANCER = "FREELANCER", "Freelancer"
    MERCHANT = "MERCHANT", "Merchant"
    JOINT = "JOINT", "Joint"
    

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
