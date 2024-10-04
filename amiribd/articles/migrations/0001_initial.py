# Generated by Django 5.0.6 on 2024-08-29 07:23

import django.utils.timezone
import django_ckeditor_5.fields
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AIHistory",
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
                ("title", models.CharField(max_length=1000)),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True, editable=False, populate_from="title"
                    ),
                ),
                ("question", models.TextField()),
                ("response", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "History",
                "verbose_name_plural": "Histories",
            },
        ),
        migrations.CreateModel(
            name="AiToken",
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
                    "tokens",
                    models.FloatField(
                        default=15.0,
                        help_text="Each article consumes 0.95 tokens. Refresh every 24 hours",
                    ),
                ),
                ("consumed_tokens", models.IntegerField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name="Article",
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
                ("title", models.CharField(max_length=200)),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True, editable=False, populate_from="title"
                    ),
                ),
                ("summary", models.TextField(blank=True)),
                (
                    "content",
                    django_ckeditor_5.fields.CKEditor5Field(verbose_name="Content"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "release_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="Time for your post to be visible to audience.",
                    ),
                ),
                ("views", models.IntegerField(default=0)),
                (
                    "cover",
                    models.FileField(
                        blank=True, null=True, upload_to="template/category"
                    ),
                ),
                ("archived", models.BooleanField(default=False)),
                ("featured", models.BooleanField(default=False)),
                ("reads", models.IntegerField(default=0)),
                ("editorsPick", models.BooleanField(default=False)),
                ("sponsored", models.BooleanField(default=False)),
                ("recommeded", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Template",
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
                ("is_premium", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Template",
                "verbose_name_plural": "Templates",
            },
        ),
        migrations.CreateModel(
            name="TemplateCategory",
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
                    "title",
                    models.CharField(
                        help_text="Blog, Youtube description",
                        max_length=100,
                        unique=True,
                    ),
                ),
                ("description", models.TextField(max_length=500)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "icon",
                    models.CharField(default="icon ni ni-spark-fill", max_length=100),
                ),
                (
                    "color",
                    models.CharField(
                        choices=[
                            ("primary", "primary"),
                            ("secondary", "secondary"),
                            ("danger", "danger"),
                            ("info", "info"),
                            ("warning", "warning"),
                            ("success", "success"),
                        ],
                        default="primary",
                        max_length=100,
                    ),
                ),
                (
                    "cover",
                    models.FileField(
                        blank=True, null=True, upload_to="template/category"
                    ),
                ),
            ],
            options={
                "verbose_name": "Template Category",
                "verbose_name_plural": "Template Categories",
            },
        ),
        migrations.CreateModel(
            name="YtSummarizer",
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
                ("title", models.CharField(blank=True, max_length=100)),
                ("video_url", models.URLField(max_length=255)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("summary", models.TextField(blank=True)),
                ("transcript_file", models.URLField(blank=True)),
                ("audio_url", models.URLField(blank=True, max_length=300)),
                ("is_processed", models.BooleanField(default=False)),
                ("duration", models.IntegerField(default=0, help_text="in seconds")),
                ("size", models.IntegerField(default=0, help_text="megabytes")),
                ("video_transcript", models.TextField(blank=True)),
                ("is_verified", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "YtSummarizer",
                "verbose_name_plural": "YtSummarizers",
            },
        ),
    ]
