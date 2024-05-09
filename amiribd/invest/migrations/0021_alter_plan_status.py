# Generated by Django 5.0.4 on 2024-05-09 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0020_accounteventwithdrawal_payment_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='status',
            field=models.CharField(choices=[('RUNNING', 'Running'), ('STOPPED', 'Stopped'), ('CANCELLED', 'Cancelled')], default='RUNNING', max_length=20),
        ),
    ]
