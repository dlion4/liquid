# Generated by Django 5.0.4 on 2024-05-05 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_alter_user_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="registration_completed",
        ),
    ]
