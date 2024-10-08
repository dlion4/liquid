# Generated by Django 5.0.6 on 2024-10-05 11:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0003_job_is_completed_job_is_rejected"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobApplicationSubmission",
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
                ("submission_data", models.DateTimeField(auto_now_add=True)),
                ("submission_file", models.FileField(upload_to="submissions/")),
                ("approved", models.BooleanField(default=False)),
                (
                    "job_application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="jobs_submissions",
                        to="jobs.job",
                    ),
                ),
                (
                    "uploader",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="submitted_by",
                        to="users.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Job Application Submission",
                "verbose_name_plural": "Job Application Submissions",
            },
        ),
    ]
