# Generated by Django 5.0.6 on 2024-10-29 15:16

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
                default=uuid.UUID("7481e95c-17ba-4a37-9658-74b87dd7b33a"),
                editable=False,
            ),
        ),
    ]