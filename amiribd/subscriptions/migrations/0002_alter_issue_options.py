# Generated by Django 5.0.6 on 2024-06-28 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="issue",
            options={"verbose_name": "Issue", "verbose_name_plural": "Issues"},
        ),
    ]
