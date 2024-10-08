# Generated by Django 5.0.6 on 2024-08-29 07:23

import amiribd.schemes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WhatsAppEarningScheme",
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
                    "views",
                    models.PositiveBigIntegerField(
                        default=0, help_text="Total number of views"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("approved", models.BooleanField(default=False)),
                ("approved_at", models.DateTimeField(auto_now=True)),
                ("rejected", models.BooleanField(default=False)),
                ("rejected_at", models.DateTimeField(auto_now=True)),
                (
                    "file",
                    models.FileField(
                        upload_to=amiribd.schemes.models.file_user_directory_path
                    ),
                ),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=1.0, max_digits=10),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
