# Generated by Django 5.0.4 on 2024-05-16 16:00

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0039_alter_token_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.UUIDField(default=uuid.UUID('db2b084e-7bc2-45ad-81b4-dadd71de5143'), editable=False),
        ),
    ]
