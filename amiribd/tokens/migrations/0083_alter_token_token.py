# Generated by Django 5.0.6 on 2024-06-05 14:40

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0082_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("ef0c286b-d1f6-454f-895a-15222da12bdf"),
                editable=False,
            ),
        ),
    ]
