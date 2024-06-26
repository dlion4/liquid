# Generated by Django 5.0.6 on 2024-06-19 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="KenyaConversion",
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
                ("country", models.CharField(max_length=100)),
                ("currency_code", models.CharField(max_length=100)),
                (
                    "currency_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "amount",
                    models.PositiveIntegerField(
                        default=10, help_text="In relation to 1 KShs"
                    ),
                ),
                (
                    "conversion_rate",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="kenyaconversion",
            constraint=models.UniqueConstraint(
                fields=("country", "currency_code"), name="unique_country_currency_code"
            ),
        ),
    ]
