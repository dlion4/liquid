# Generated by Django 5.0.4 on 2024-05-10 14:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0008_alter_token_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.UUIDField(default=uuid.UUID('09a57625-6b09-4d7d-9c8a-8b58c7dcce21'), editable=False),
        ),
    ]
