# Generated by Django 5.0.4 on 2024-05-09 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0022_accounteventwithdrawal_paid'),
        ('transactions', '0006_alter_transaction_options'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AccountEventWithdrawal',
            new_name='AccountWithdrawalAction',
        ),
    ]