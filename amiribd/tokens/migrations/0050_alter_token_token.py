# Generated by Django 5.0.4 on 2024-05-18 04:59

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0049_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("02da3628-a15a-42e0-892b-f23c7993ac35"),
                editable=False,
            ),
        ),
    ]
