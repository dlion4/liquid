# Generated by Django 5.0.4 on 2024-05-07 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("invest", "0003_accounttype_alter_account_type"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Transaction",
        ),
    ]
