# Generated by Django 5.0.6 on 2024-06-19 10:59

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0087_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("7ec97059-3e4a-485d-a452-ba5d0e22768c"),
                editable=False,
            ),
        ),
    ]
