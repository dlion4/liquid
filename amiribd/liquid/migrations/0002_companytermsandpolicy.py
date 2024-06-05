# Generated by Django 5.0.6 on 2024-06-05 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("liquid", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompanyTermsAndPolicy",
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
                ("file", models.FileField(upload_to="policy")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
