# Generated by Django 5.1.4 on 2024-12-06 16:37

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0047_alter_token_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.UUIDField(default=uuid.UUID('f4b5e5c7-bb27-4e13-b6a4-42ec29c40138'), editable=False),
        ),
    ]
