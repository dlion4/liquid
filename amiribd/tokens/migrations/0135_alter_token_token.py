# Generated by Django 5.0.6 on 2024-07-03 20:49

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0134_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("4d340419-f5ce-4dfe-b5d0-20fb4b173fa8"),
                editable=False,
            ),
        ),
    ]