# Generated by Django 5.0.4 on 2024-05-21 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="title",
            field=models.CharField(max_length=200),
        ),
    ]
