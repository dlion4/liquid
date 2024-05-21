# Generated by Django 5.0.4 on 2024-05-21 04:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transactions', '0007_transaction_is_payment_success_and_more'),
        ('users', '0026_remove_profile_plans'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('channel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.paymentmethod')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_payment_channel', to='users.profile')),
            ],
        ),
    ]