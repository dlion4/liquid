# Generated by Django 5.0.6 on 2024-07-11 07:46

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0155_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("556af09f-8c5b-4616-bc82-c9c35fd0b59b"),
                editable=False,
            ),
        ),
    ]
