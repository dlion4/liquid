# Generated by Django 5.0.4 on 2024-05-14 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_alter_plantformtype_options_alter_agent_plantform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='plantform',
            field=models.ManyToManyField(blank=True, related_name='plantforms', to='profiles.plantform'),
        ),
    ]
