# Generated by Django 5.0.6 on 2024-07-09 13:02

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0139_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("15e38730-e806-459b-81f9-9a07765ccdee"),
                editable=False,
            ),
        ),
    ]
