# Generated by Django 5.0.4 on 2024-05-15 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0026_plantype_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]