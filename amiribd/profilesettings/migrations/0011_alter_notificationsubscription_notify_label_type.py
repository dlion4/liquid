# Generated by Django 5.0.4 on 2024-05-10 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profilesettings", "0010_notificationsubscription_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notificationsubscription",
            name="notify_label_type",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="notify_label_type",
                to="profilesettings.notificationtype",
            ),
        ),
    ]
