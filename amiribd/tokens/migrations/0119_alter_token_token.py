# Generated by Django 5.0.6 on 2024-06-30 17:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0118_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("858b1d72-e8b1-4c8c-9fcc-2347c4cad79f"),
                editable=False,
            ),
        ),
    ]
