# Generated by Django 5.0.4 on 2024-05-19 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0032_plantype_svg'),
        ('users', '0024_profile_referred_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='plans',
            field=models.ManyToManyField(blank=True, to='invest.plan'),
        ),
    ]
