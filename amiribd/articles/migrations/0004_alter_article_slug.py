# Generated by Django 5.0.4 on 2024-05-21 13:22

import django_extensions.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_article_created_at_article_profile_article_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title'),
        ),
    ]
