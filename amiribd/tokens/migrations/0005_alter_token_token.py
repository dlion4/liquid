# Generated by Django 5.0.6 on 2024-10-05 11:40

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0004_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("c4fbe821-3704-4bd9-b7d5-838149c8ac1d"),
                editable=False,
            ),
        ),
    ]
