# Generated by Django 5.0.4 on 2024-05-06 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0015_alter_profile_date_of_birth"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="correct_information",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="document",
            name="read_terms",
            field=models.BooleanField(default=False),
        ),
    ]
