# Generated by Django 5.0.6 on 2024-06-04 13:48

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0070_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("303b6b57-9079-4cba-bfe7-14cfbf45259e"),
                editable=False,
            ),
        ),
    ]
