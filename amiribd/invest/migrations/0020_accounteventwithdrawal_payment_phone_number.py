# Generated by Django 5.0.4 on 2024-05-09 09:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0019_accounteventdeposit_accounteventwithdrawal_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounteventwithdrawal',
            name='payment_phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must start with a digit and be 9 to 15 digits in total.', regex='^[0-9]\\d{8,14}$')]),
        ),
    ]
