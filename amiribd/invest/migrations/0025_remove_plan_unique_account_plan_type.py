# Generated by Django 5.0.4 on 2024-05-12 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0024_plan_unique_account_plan_type'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='plan',
            name='unique_account_plan_type',
        ),
    ]
