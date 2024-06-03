# Generated by Django 5.0.4 on 2024-05-10 12:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profilesettings", "0001_initial"),
        ("users", "0024_profile_referred_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notificationtype",
            name="profile",
            field=models.ManyToManyField(
                blank=True, related_name="profile_notifications", to="users.profile"
            ),
        ),
        migrations.CreateModel(
            name="Notify",
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
                    "notify_label_type",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="notify_type_label",
                        to="profilesettings.notificationtype",
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.profile"
                    ),
                ),
            ],
        ),
    ]
