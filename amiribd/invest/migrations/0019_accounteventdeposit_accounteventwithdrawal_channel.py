# Generated by Django 5.0.4 on 2024-05-09 08:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0018_accounteventwithdrawal_withdrawal_date_and_more'),
        ('transactions', '0006_alter_transaction_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountEventDeposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='accounteventwithdrawal',
            name='channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_channel_account_event', to='transactions.paymentmethod'),
        ),
    ]