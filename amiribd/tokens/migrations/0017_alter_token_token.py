# Generated by Django 5.0.4 on 2024-05-12 11:25

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0016_alter_token_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.UUIDField(default=uuid.UUID('55730335-db2c-4286-9eb7-60e4a04e2c83'), editable=False),
        ),
    ]
