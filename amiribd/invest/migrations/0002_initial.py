# Generated by Django 5.0.6 on 2024-08-29 07:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("invest", "0001_initial"),
        ("transactions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="accountwithdrawalaction",
            name="channel",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payment_channel_account_event",
                to="transactions.paymentmethod",
            ),
        ),
        migrations.AddField(
            model_name="plan",
            name="account",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="account_plan",
                to="invest.account",
            ),
        ),
        migrations.AddField(
            model_name="plan",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="plan_type",
                to="invest.plantype",
                verbose_name="Plan",
            ),
        ),
    ]