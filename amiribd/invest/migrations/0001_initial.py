# Generated by Django 5.0.4 on 2024-05-06 21:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0024_profile_referred_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('BASIC', 'Basic'), ('STANDARD', 'Standard')], default='BASIC', max_length=10)),
                ('fee', models.DecimalField(decimal_places=2, default=300.0, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('balance', models.DecimalField(decimal_places=2, default=300.0, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(choices=[('BRONZE', '  Bronze'), ('SILVER', '  Silver'), ('DIAMOND', '  Diamond')], default='BRONZE', max_length=15)),
                ('min_amount', models.DecimalField(decimal_places=2, default=300.0, max_digits=15)),
                ('max_amount', models.DecimalField(decimal_places=2, default=300.0, max_digits=15)),
                ('fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=11)),
                ('percentage_return', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('RUNNING', 'Running'), ('STOPPED', 'Stopped'), ('SUSPENDED', 'Suspended')], default='RUNNING', max_length=20)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_plan', to='invest.account')),
            ],
        ),
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('INDIVIDUAL', 'Individual'), ('FAMILY', 'Family'), ('JOINT', 'Joint'), ('INSTITUTON', 'Instituton')], default='INDIVIDUAL', max_length=25)),
                ('fee', models.DecimalField(decimal_places=2, default=300.0, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account_profile', to='users.profile')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='pool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_pool', to='invest.pool'),
        ),
        migrations.CreateModel(
            name='PoolFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.TextField(blank=True, null=True)),
                ('pool', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pool_feature', to='invest.pool')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('DEPOSIT', 'Deposit'), ('WITHDRAWAL', 'Withdrawal')], max_length=22)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('verified', models.BooleanField(default=False)),
                ('receipt_number', models.CharField(blank=True, max_length=255, null=True)),
                ('source', models.CharField(blank=True, max_length=255, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_account', to='invest.account')),
            ],
        ),
    ]
