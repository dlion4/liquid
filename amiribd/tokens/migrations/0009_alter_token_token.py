# Generated by Django 5.0.6 on 2024-10-08 04:08

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0008_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("50dcded3-e329-40ed-8ede-1b45236af34f"),
                editable=False,
            ),
        ),
    ]