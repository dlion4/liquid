# Generated by Django 5.0.6 on 2024-10-08 04:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "jobs",
            "0005_rename_submission_data_jobapplicationsubmission_submission_date",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="job",
            options={"ordering": ["-id"]},
        ),
    ]
