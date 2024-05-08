# Generated by Django 5.0.4 on 2024-05-08 10:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0011_alter_account_pool'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='percentage_return',
        ),
        migrations.AddField(
            model_name='plantype',
            name='percentage_return',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_type', to='invest.accounttype', verbose_name='account_type'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_type', to='invest.plantype', verbose_name='Plan'),
        ),
    ]
