# Generated by Django 5.0.6 on 2024-06-28 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0008_templatecategory_icon_alter_aitoken_profile_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AIHistory",
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
                ("title", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "History",
                "verbose_name_plural": "Histories",
            },
        ),
    ]
