# Generated by Django 5.0.6 on 2024-06-30 11:10

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0116_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("30fd5d93-0404-45be-a78c-d51429acdfc1"),
                editable=False,
            ),
        ),
    ]
