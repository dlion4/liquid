# Generated by Django 5.0.4 on 2024-05-10 12:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("79e5a102-e571-436c-979a-775370ed953c"),
                editable=False,
            ),
        ),
    ]
