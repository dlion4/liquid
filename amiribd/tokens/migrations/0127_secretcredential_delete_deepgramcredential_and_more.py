# Generated by Django 5.0.6 on 2024-07-02 09:03

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0126_deepgramcredential_alter_token_token"),
    ]

    operations = [
        migrations.CreateModel(
            name="SecretCredential",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("email", models.EmailField(blank=True, max_length=100, null=True)),
                ("project_id", models.UUIDField(blank=True, null=True)),
                (
                    "secret_key",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                ("api_key", models.CharField(max_length=3000)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "DeepGram Credential",
                "verbose_name_plural": "DeepGram Credentials",
            },
        ),
        migrations.DeleteModel(
            name="DeepGramCredential",
        ),
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.UUIDField(
                default=uuid.UUID("35581812-9e64-497a-b311-507bbedc304c"),
                editable=False,
            ),
        ),
    ]
