# Generated by Django 5.0.6 on 2024-06-05 08:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0081_alter_token_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("9c29a0fb-5261-43c7-85ee-afd9014cdf3b"),
                editable=False,
            ),
        ),
    ]
