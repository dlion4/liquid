# Generated by Django 5.0.6 on 2024-07-09 21:33

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0140_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("169bfec1-9e7b-424d-a3a8-77864aa44faf"),
                editable=False,
            ),
        ),
    ]
