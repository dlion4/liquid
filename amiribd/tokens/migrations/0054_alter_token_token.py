# Generated by Django 5.0.4 on 2024-05-19 23:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0053_alter_token_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.UUIDField(default=uuid.UUID('5e1111af-6e8c-4d70-a34b-dcd288f88b00'), editable=False),
        ),
    ]
