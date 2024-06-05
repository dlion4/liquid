# Generated by Django 5.0.6 on 2024-06-05 05:24

import amiribd.jobs.models
import django.db.models.deletion
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0026_remove_profile_plans"),
    ]

    operations = [
        migrations.CreateModel(
            name="Job",
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
                ("title", models.CharField(max_length=255)),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True, editable=False, populate_from="title"
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        help_text="online, Nairobi, Qatar, etc", max_length=255
                    ),
                ),
                ("description", models.TextField()),
                ("date_posted", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.profile",
                        verbose_name="Job Author",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JobApplication",
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
                    "resume",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=amiribd.jobs.models.upload_application_resume,
                    ),
                ),
                ("cover_letter", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("ACCEPTED", "Accepted"),
                            ("REJECTED", "Rejected"),
                        ],
                        default="PENDING",
                        max_length=10,
                    ),
                ),
                (
                    "email_or_phone",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "applicant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.profile"
                    ),
                ),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="applications",
                        to="jobs.job",
                    ),
                ),
            ],
        ),
    ]
