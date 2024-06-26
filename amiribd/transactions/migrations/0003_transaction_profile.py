# Generated by Django 5.0.4 on 2024-05-07 14:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0002_alter_paymentmethod_icon"),
        ("users", "0024_profile_referred_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="profile",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="users.profile",
            ),
        ),
    ]
