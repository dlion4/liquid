# Generated by Django 5.0.6 on 2024-10-09 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_validatedemailaddress_options"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ValidatedEmailAddress",
        ),
    ]