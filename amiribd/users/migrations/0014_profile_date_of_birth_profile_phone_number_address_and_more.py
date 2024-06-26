# Generated by Django 5.0.4 on 2024-05-05 18:50

import amiribd.users.models
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0013_profile_kyc_completed_profile_kyc_completed_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="phone_number",
            field=models.CharField(
                blank=True,
                max_length=20,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Phone number must start with a digit and be 9 to 15 digits in total.",
                        regex="^[0-9]\\d{8,14}$",
                    )
                ],
            ),
        ),
        migrations.CreateModel(
            name="Address",
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
                ("addr_line1", models.CharField(max_length=255)),
                ("addr_line2", models.CharField(blank=True, max_length=255, null=True)),
                ("city", models.CharField(max_length=255)),
                ("state", models.CharField(max_length=255)),
                ("country", models.CharField(max_length=255)),
                ("zip_code", models.CharField(max_length=255)),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile_address",
                        to="users.profile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Document",
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
                ("document_type", models.CharField(default="NI", max_length=2)),
                (
                    "document",
                    models.ImageField(
                        upload_to=amiribd.users.models.user_directory_path
                    ),
                ),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile_document",
                        to="users.profile",
                    ),
                ),
            ],
        ),
    ]
