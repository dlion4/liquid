# Generated by Django 5.0.6 on 2024-06-01 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invest", "0032_plantype_svg"),
    ]

    operations = [
        migrations.AddField(
            model_name="plan",
            name="mpesa_transaction_code",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]