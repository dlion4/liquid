# Generated by Django 5.0.4 on 2024-05-10 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("profilesettings", "0008_alter_notificationsubscription_notify_label_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="notificationsubscription",
            name="profile",
        ),
    ]
