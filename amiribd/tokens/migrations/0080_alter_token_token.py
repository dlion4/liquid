# Generated by Django 5.0.6 on 2024-06-05 06:51

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0079_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("e735ff32-45a0-45ff-889d-19fd5fa3bb09"),
                editable=False,
            ),
        ),
    ]