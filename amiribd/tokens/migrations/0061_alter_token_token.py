# Generated by Django 5.0.6 on 2024-05-21 21:47

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0060_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("d8c1aa9a-230b-4876-8365-4d55c572d1d4"),
                editable=False,
            ),
        ),
    ]
