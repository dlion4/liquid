# Generated by Django 5.0.6 on 2024-07-01 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0016_article_recommeded"),
        ("users", "0031_alter_profile_image"),
    ]

    operations = [
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
                ("video_url", models.URLField(max_length=255)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("summary", models.TextField(blank=True)),
                ("audio_file", models.URLField(blank=True, max_length=2000, null=True)),
                ("is_processed", models.BooleanField(default=False)),
                (
                    "profile",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "YtSummarizer",
                "verbose_name_plural": "YtSummarizers",
            },
        ),
    ]
