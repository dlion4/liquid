# Generated by Django 5.0.4 on 2024-05-18 05:08

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0050_alter_token_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.UUIDField(default=uuid.UUID('7623b94b-89f6-4855-b804-a8aa47658593'), editable=False),
        ),
    ]