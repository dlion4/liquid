# Generated by Django 5.0.6 on 2024-07-11 08:25

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0163_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("2c1be023-07ac-4b70-ac84-d37760c806b8"),
                editable=False,
            ),
        ),
    ]
