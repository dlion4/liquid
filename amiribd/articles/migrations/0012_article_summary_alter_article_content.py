# Generated by Django 5.0.6 on 2024-06-30 11:10

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0011_aihistory_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="summary",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="content",
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name="Content"),
        ),
    ]
