# Generated by Django 5.0.4 on 2024-05-17 10:19

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0044_alter_token_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.UUIDField(default=uuid.UUID('c6adc277-d536-411e-ba89-5fe7e5f4fb03'), editable=False),
        ),
    ]
