# Generated by Django 5.0.6 on 2024-10-05 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0004_jobapplicationsubmission"),
    ]

    operations = [
        migrations.RenameField(
            model_name="jobapplicationsubmission",
            old_name="submission_data",
            new_name="submission_date",
        ),
    ]