# Generated by Django 5.0.6 on 2024-06-26 05:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0098_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("693a39e0-b7b8-47df-a5f4-1e59eedcdc83"),
                editable=False,
            ),
        ),
    ]