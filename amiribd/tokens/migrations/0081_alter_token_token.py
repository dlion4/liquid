# Generated by Django 5.0.6 on 2024-06-05 08:28

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0080_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("ea704090-5b17-49bc-9d33-01769a51eca5"),
                editable=False,
            ),
        ),
    ]