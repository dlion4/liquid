# Generated by Django 5.0.4 on 2024-05-16 17:42

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0040_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("fb7ab4e9-33f4-47ae-a8e5-8560f775ef47"),
                editable=False,
            ),
        ),
    ]
