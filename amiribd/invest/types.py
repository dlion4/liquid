from django.db import models


class PoolType(models.TextChoices):
    INDIVIDUAL = "INDIVIDUAL", "Individual"
    FAMILY = "FAMILY", "Family"
    JOINT = "JOINT", "Joint"
    INSTITUTON = "INSTITUTON", "Instituton"


class AccountType(models.TextChoices):
    BASIC = "BASIC", "Basic"
    STANDARD = "STANDARD", "Standard"


class PlanType(models.TextChoices):
    BRONZE = "BRONZE", "  Bronze"
    SILVER = "SILVER", "  Silver"
    DIAMOND = "DIAMOND", "  Diamond"


class PlanStatus(models.TextChoices):
    RUNNING = "RUNNING", "Running"
    STOPPED = "STOPPED", "Stopped"
    SUSPENDED = "SUSPENDED", "Suspended"


class TransactionType(models.TextChoices):
    DEPOSIT = "DEPOSIT", "Deposit"
    WITHDRAWAL = "WITHDRAWAL", "Withdrawal"
