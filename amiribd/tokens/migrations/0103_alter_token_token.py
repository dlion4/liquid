# Generated by Django 5.0.6 on 2024-06-28 06:18

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0102_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("afdb9c5d-aa0a-41ec-a3e8-63e917dee856"),
                editable=False,
            ),
        ),
    ]
