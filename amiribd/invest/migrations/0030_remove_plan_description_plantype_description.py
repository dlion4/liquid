# Generated by Django 5.0.4 on 2024-05-16 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0029_alter_plan_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='description',
        ),
        migrations.AddField(
            model_name='plantype',
            name='description',
            field=models.TextField(blank=True, default='Unlimited access with priority support, 99.95% uptime, powerfull features and more...', help_text='Description', max_length=300, null=True),
        ),
    ]
