# Generated by Django 5.0.6 on 2024-10-19 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_delete_validatedemailaddress"),
    ]

    operations = [
        migrations.CreateModel(
            name="ValidatedEmailAddress",
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
                ("email_address", models.EmailField(max_length=300, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Validated Email Address",
                "verbose_name_plural": "Validated Email Address",
            },
        ),
    ]
