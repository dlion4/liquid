# Generated by Django 5.0.6 on 2024-07-11 08:10

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0160_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("9b29dd38-95aa-46a5-8b3e-422844d41eec"),
                editable=False,
            ),
        ),
    ]
