# Generated by Django 5.0.4 on 2024-05-12 09:23

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0015_alter_token_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.UUIDField(default=uuid.UUID('c2d83b96-3913-4651-a9b9-184575b0e35a'), editable=False),
        ),
    ]