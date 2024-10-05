# Generated by Django 5.0.6 on 2024-08-29 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Package",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("monthly_price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("annual_price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("monthly_discount", models.PositiveIntegerField(default=3)),
                ("annual_discount", models.PositiveIntegerField(default=15)),
            ],
            options={
                "verbose_name": "Package",
                "verbose_name_plural": "Packages",
            },
        ),
    ]