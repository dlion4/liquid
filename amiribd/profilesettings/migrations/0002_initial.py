# Generated by Django 5.0.6 on 2024-08-29 07:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("profilesettings", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="notificationsubscription",
            name="profile",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notification_profile_subscription",
                to="users.profile",
            ),
        ),
        migrations.AddField(
            model_name="notificationtype",
            name="notification",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="notification_types",
                to="profilesettings.notification",
            ),
        ),
        migrations.AddField(
            model_name="notificationtype",
            name="profile",
            field=models.ManyToManyField(
                blank=True, related_name="profile_notifications", to="users.profile"
            ),
        ),
        migrations.AddField(
            model_name="notificationsubscription",
            name="notify_label_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="notify_label_type",
                to="profilesettings.notificationtype",
            ),
        ),
    ]