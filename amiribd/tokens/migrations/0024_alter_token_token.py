# Generated by Django 5.0.4 on 2024-05-14 08:49

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0023_alter_token_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.UUIDField(default=uuid.UUID('45eb6e33-7b4d-490c-bab3-c0dc7cc6ccba'), editable=False),
        ),
    ]