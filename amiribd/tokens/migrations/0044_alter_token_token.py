# Generated by Django 5.0.6 on 2024-10-30 09:44

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0043_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("239e901b-ee07-449a-b9aa-1dbbfca2244b"),
                editable=False,
            ),
        ),
    ]
