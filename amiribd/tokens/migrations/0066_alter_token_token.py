# Generated by Django 5.0.6 on 2024-06-01 10:53

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0065_alter_token_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.UUIDField(default=uuid.UUID('bdd8a7a7-9e6e-4463-a244-cf90077e7004'), editable=False),
        ),
    ]
