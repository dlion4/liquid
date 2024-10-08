# Generated by Django 5.0.6 on 2024-08-29 07:23

import django.core.validators
import django.db.models.deletion
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AccountEventDeposit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AccountType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("Basic", "Basic"), ("Standard", "Standard")],
                        default="Basic",
                        max_length=10,
                    ),
                ),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Plan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True, editable=False, populate_from="type"
                    ),
                ),
                (
                    "min_amount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
                ),
                (
                    "max_amount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
                ),
                (
                    "fee",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=11),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("RUNNING", "Running"),
                            ("STOPPED", "Stopped"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="RUNNING",
                        max_length=20,
                    ),
                ),
                (
                    "payment_method",
                    models.CharField(blank=True, default="MPESA", max_length=100),
                ),
                ("sku", models.CharField(blank=True, max_length=100)),
                ("is_paid", models.BooleanField(default=False)),
                (
                    "mpesa_transaction_code",
                    models.CharField(blank=True, max_length=1000),
                ),
                ("payment_phone_number", models.CharField(blank=True, max_length=1000)),
            ],
            options={
                "get_latest_by": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="PlanType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("BRONZE", "  Bronze"),
                            ("SILVER", "  Silver"),
                            ("DIAMOND", "  Diamond"),
                        ],
                        default="BRONZE",
                        max_length=15,
                    ),
                ),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
                ),
                ("percentage_return", models.FloatField(default=0)),
                ("icon", models.CharField(blank=True, default="", max_length=100)),
                ("svg", models.FileField(blank=True, null=True, upload_to="icons/")),
                (
                    "interval",
                    models.CharField(
                        blank=True,
                        default="Unlimited",
                        help_text="Interval ie Monthly, Yearly, Unlimited",
                        max_length=100,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        default="Unlimited access with priority support, 99.95% uptime, powerful features and more...",
                        help_text="Description",
                        max_length=500,
                    ),
                ),
                (
                    "theme",
                    models.CharField(
                        choices=[
                            ("primary", "primary"),
                            ("secondary", "secondary"),
                            ("danger", "danger"),
                            ("info", "info"),
                            ("success", "success"),
                            ("orange", "orange"),
                            ("teal", "teal"),
                            ("pink", "pink"),
                            ("azure", "azure"),
                        ],
                        default="orange",
                        max_length=100,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Pool",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Pool",
                "verbose_name_plural": "Pools",
            },
        ),
        migrations.CreateModel(
            name="PoolFeature",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("feature", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="PoolType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("INDIVIDUAL", "Individual"),
                            ("FAMILY", "Family"),
                            ("JOINT", "Joint"),
                            ("INSTITUTON", "Instituton"),
                        ],
                        default="INDIVIDUAL",
                        max_length=12,
                        unique=True,
                    ),
                ),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SavingInvestmentPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("approved", "approved"),
                            ("declined", "declined"),
                            ("expired", "expired"),
                        ],
                        default="pending",
                        max_length=100,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SavingPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                (
                    "interest",
                    models.FloatField(
                        default=1, help_text="The interest rate charged daily"
                    ),
                ),
                (
                    "term",
                    models.IntegerField(
                        default=1, help_text="Maturation term. Example value 3 days"
                    ),
                ),
                (
                    "principal",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        help_text="Investment amount",
                        max_digits=15,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        default="Choose your investment plan and start earning.",
                        max_length=300,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "balance",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
                ),
                ("account_ssid", models.CharField(blank=True, max_length=200)),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="account_type",
                        to="invest.accounttype",
                        verbose_name="account_type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Account",
                "verbose_name_plural": "Accounts",
            },
        ),
        migrations.CreateModel(
            name="AccountWithdrawalAction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "action",
                    models.CharField(
                        blank=True,
                        choices=[("Withdrawal", "Withdrawal"), ("Deposit", "Deposit")],
                        default="Withdrawal",
                        max_length=100,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Initiated", "Initiated"),
                            ("Resolved", "Resolved"),
                            ("Cancelled", "Cancelled"),
                        ],
                        default="Initiated",
                        max_length=100,
                    ),
                ),
                ("withdrawal_date", models.DateField(blank=True, null=True)),
                ("withdrawal_time", models.TimeField(blank=True, null=True)),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "payment_phone_number",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must start with a digit and be 9 to 15 digits in total.",
                                regex="^[0-9]\\d{8,14}$",
                            )
                        ],
                    ),
                ),
                ("paid", models.BooleanField(default=False)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="account_event_action",
                        to="invest.account",
                    ),
                ),
            ],
        ),
    ]
