# Generated by Django 5.0.4 on 2024-05-14 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_remove_plantform_agent_agent_plantform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='plantform',
            field=models.ManyToManyField(blank=True, related_name='agent_plantform', to='profiles.plantform'),
        ),
    ]