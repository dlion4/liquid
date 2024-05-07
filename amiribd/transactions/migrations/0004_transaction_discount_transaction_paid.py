# Generated by Django 5.0.4 on 2024-05-07 14:41

import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_transaction_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='transaction',
            name='paid',
            field=models.GeneratedField(db_persist=True, expression=django.db.models.expressions.CombinedExpression(models.F('amount'), '-', models.F('discount')), output_field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
        ),
    ]
