# Generated by Django 5.0.6 on 2024-10-09 12:43

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0018_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("a5f8557c-273f-4875-8517-c58df88b35d9"),
                editable=False,
            ),
        ),
    ]
