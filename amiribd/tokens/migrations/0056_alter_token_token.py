# Generated by Django 5.0.4 on 2024-05-20 13:29

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0055_alter_token_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.UUIDField(default=uuid.UUID('16e712f3-afab-46ee-a172-50c3b33e3160'), editable=False),
        ),
    ]