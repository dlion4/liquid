# Generated by Django 5.0.6 on 2024-06-05 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0002_job_content_alter_job_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="level",
            field=models.CharField(
                choices=[("A", "Advanced"), ("B", "Beginner"), ("I", "Intermediate")],
                default="B",
                max_length=1,
            ),
        ),
    ]
