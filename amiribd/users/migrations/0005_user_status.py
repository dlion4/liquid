# Generated by Django 5.0.4 on 2024-05-05 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_registration_completed_user_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('completed', 'completed'), ('blocked', 'blocked'), ('suspended', 'suspended')], default='pending', max_length=255),
        ),
    ]
