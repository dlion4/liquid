# Generated by Django 5.0.4 on 2024-05-17 08:28

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0041_alter_token_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.UUIDField(default=uuid.UUID('0add5d9e-7e6e-4200-8353-029071cc3153'), editable=False),
        ),
    ]