# Generated by Django 5.0.6 on 2024-10-27 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_validatedemailaddress"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="has_plan",
            field=models.BooleanField(default=False),
        ),
    ]