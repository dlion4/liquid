# Generated by Django 5.0.4 on 2024-05-08 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0014_alter_plan_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='payment_method',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
