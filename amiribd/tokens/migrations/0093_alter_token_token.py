# Generated by Django 5.0.6 on 2024-06-22 22:30

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0092_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("b42f2799-4085-4b75-87cf-5da6a95aa0b4"),
                editable=False,
            ),
        ),
    ]
