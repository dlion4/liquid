# Generated by Django 5.0.6 on 2024-05-21 04:56

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0059_alter_token_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.UUIDField(default=uuid.UUID('20eefe31-144f-4fb8-81a0-9c3b7ed14194'), editable=False),
        ),
    ]
