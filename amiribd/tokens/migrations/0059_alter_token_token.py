# Generated by Django 5.0.4 on 2024-05-21 12:25

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0058_alter_token_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.UUIDField(default=uuid.UUID('636ee374-2498-4f2d-b3b4-df3332fc49b7'), editable=False),
        ),
    ]
