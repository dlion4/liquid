# Generated by Django 5.0.4 on 2024-05-13 11:33

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0020_alter_token_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.UUIDField(default=uuid.UUID('32c0d62f-7673-4792-8e06-a618092309e2'), editable=False),
        ),
    ]
