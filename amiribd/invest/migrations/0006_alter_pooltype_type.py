# Generated by Django 5.0.6 on 2024-10-08 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invest", "0005_alter_pooltype_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pooltype",
            name="type",
            field=models.CharField(
                choices=[
                    ("INDIVIDUAL", "Individual"),
                    ("MERCHANT", "Merchant"),
                    ("JOINT", "Joint"),
                    ("FREELANCE", "Freelance"),
                ],
                default="INDIVIDUAL",
                max_length=10,
                unique=True,
            ),
        ),
    ]
