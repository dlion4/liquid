# Generated by Django 5.0.6 on 2024-05-12 14:01

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0018_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("94e7c20d-a97b-4af7-aa48-9a9d6debe02e"),
                editable=False,
            ),
        ),
    ]
