# Generated by Django 5.0.6 on 2024-07-11 08:48

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0165_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("9f8ee719-deda-47d5-83f5-9abc8a372f7f"),
                editable=False,
            ),
        ),
    ]