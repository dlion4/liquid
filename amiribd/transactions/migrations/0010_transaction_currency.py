# Generated by Django 5.0.6 on 2024-06-20 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0009_transaction_payment_phone_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="currency",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
