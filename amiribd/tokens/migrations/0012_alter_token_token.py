# Generated by Django 5.0.6 on 2024-10-08 06:53

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0011_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("6ef02e7f-14d3-45f6-be6d-b39cf1da4554"),
                editable=False,
            ),
        ),
    ]