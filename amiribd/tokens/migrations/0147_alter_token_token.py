# Generated by Django 5.0.6 on 2024-07-11 06:53

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0146_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("b8ffd2d7-aa18-4afb-bd97-ea546cca39d2"),
                editable=False,
            ),
        ),
    ]
