# Generated by Django 5.0.6 on 2024-06-04 16:02

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0072_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("c4f78090-4c52-4dc5-95cc-7cf9c56fdd75"),
                editable=False,
            ),
        ),
    ]
