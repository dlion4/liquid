# Generated by Django 5.0.6 on 2024-06-20 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0010_transaction_currency"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
