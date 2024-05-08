# Generated by Django 5.0.4 on 2024-05-07 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0007_alter_accounttype_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttype',
            name='type',
            field=models.CharField(choices=[('Basic', 'Basic'), ('Standard', 'Standard')], default='Basic', max_length=10, unique=True),
        ),
    ]