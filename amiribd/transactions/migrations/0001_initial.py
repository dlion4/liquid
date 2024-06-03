# Generated by Django 5.0.4 on 2024-05-07 12:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("invest", "0004_delete_transaction"),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentMethod",
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
                ("channel", models.CharField(max_length=255)),
                ("icon", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
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
                        choices=[("DEPOSIT", "Deposit"), ("WITHDRAWAL", "Withdrawal")],
                        max_length=22,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
                ),
                ("verified", models.BooleanField(default=False)),
                (
                    "receipt_number",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("source", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transaction_account",
                        to="invest.account",
                    ),
                ),
            ],
        ),
    ]
