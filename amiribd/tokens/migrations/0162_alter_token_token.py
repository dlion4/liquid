# Generated by Django 5.0.6 on 2024-07-11 08:14

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0161_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("0f2c2945-12f7-4169-a02a-a8629d2efa70"),
                editable=False,
            ),
        ),
    ]
