# Generated by Django 5.0.4 on 2024-05-14 07:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0024_profile_referred_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Position',
                'verbose_name_plural': 'Positions',
            },
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_agent', to='users.profile')),
                ('position', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='agent_position', to='profiles.position')),
            ],
            options={
                'verbose_name': 'Agent',
                'verbose_name_plural': 'Agents',
            },
        ),
        migrations.CreateModel(
            name='Plantform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertisement_plantforms', to='profiles.agent')),
            ],
            options={
                'verbose_name': 'Plantform',
                'verbose_name_plural': 'Plantforms',
            },
        ),
    ]