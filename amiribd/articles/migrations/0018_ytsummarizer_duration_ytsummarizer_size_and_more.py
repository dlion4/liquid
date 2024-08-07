# Generated by Django 5.0.6 on 2024-07-01 18:20

import amiribd.articles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0017_ytsummarizer"),
    ]

    operations = [
        migrations.AddField(
            model_name="ytsummarizer",
            name="duration",
            field=models.IntegerField(default=0, help_text="in seconds"),
        ),
        migrations.AddField(
            model_name="ytsummarizer",
            name="size",
            field=models.IntegerField(default=0, help_text="megabytes"),
        ),
        migrations.AlterField(
            model_name="ytsummarizer",
            name="audio_file",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=amiribd.articles.models.youtube_audio_file_path,
            ),
        ),
    ]
