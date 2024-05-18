# Generated by Django 5.0.4 on 2024-05-17 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0006_message'),
        ('users', '0024_profile_referred_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='seen',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archived_at', models.DateTimeField(auto_now_add=True)),
                ('archiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archiver_messages', to='users.profile')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archived_messages', to='streams.message')),
            ],
        ),
    ]