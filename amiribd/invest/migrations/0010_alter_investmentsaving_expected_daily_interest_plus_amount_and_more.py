# Generated by Django 5.0.6 on 2024-10-30 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invest", "0009_alter_pooltype_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="investmentsaving",
            name="expected_daily_interest_plus_amount",
            field=models.CharField(default=0.0, max_length=12),
        ),
        migrations.AlterField(
            model_name="investmentsaving",
            name="interest_amount",
            field=models.CharField(default=0.0, max_length=12),
        ),
        migrations.AlterField(
            model_name="investmentsaving",
            name="principal_amount",
            field=models.CharField(default=0.0, max_length=12),
        ),
        migrations.AlterField(
            model_name="pooltype",
            name="type",
            field=models.CharField(
                choices=[
                    ("INDIVIDUAL", "Individual"),
                    ("FREELANCER", "Freelancer"),
                    ("MERCHANT", "Merchant"),
                    ("JOINT", "Joint"),
                ],
                default="INDIVIDUAL",
                max_length=10,
                unique=True,
            ),
        ),
    ]