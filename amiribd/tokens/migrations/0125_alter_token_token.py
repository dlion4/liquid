# Generated by Django 5.0.6 on 2024-07-02 06:41

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0124_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("3fc4a05c-5ca5-4408-a321-0db4b1769a27"),
                editable=False,
            ),
        ),
    ]
