# Generated by Django 5.0.4 on 2024-05-06 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0022_profile_initials"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="referral_code",
            field=models.CharField(blank=True, max_length=59, null=True),
        ),
    ]
