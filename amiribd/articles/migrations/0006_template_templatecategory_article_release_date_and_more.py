# Generated by Django 5.0.6 on 2024-06-28 06:18

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0005_alter_article_updated_at"),
        ("users", "0030_profile_adverts_alter_profile_plans"),
    ]

    operations = [
        migrations.CreateModel(
            name="Template",
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
                ("is_premium", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Template",
                "verbose_name_plural": "Templates",
            },
        ),
        migrations.CreateModel(
            name="TemplateCategory",
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
                (
                    "title",
                    models.CharField(
                        help_text="Blog, Youtube description",
                        max_length=100,
                        unique=True,
                    ),
                ),
                ("description", models.TextField(max_length=500)),
            ],
            options={
                "verbose_name": "Template Category",
                "verbose_name_plural": "Template Categories",
            },
        ),
        migrations.AddField(
            model_name="article",
            name="release_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                help_text="Time for your post to be visible to audience.",
            ),
        ),
        migrations.CreateModel(
            name="AiToken",
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
                (
                    "tokens",
                    models.FloatField(
                        default=15.0,
                        help_text="Each article consumes 0.95 tokens. Refresh every 24 hours",
                    ),
                ),
                ("consumed_tokens", models.IntegerField(default=0.0)),
                (
                    "profile",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.profile",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="article",
            name="template",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="article_template",
                to="articles.template",
            ),
        ),
        migrations.AddField(
            model_name="template",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="category_templates",
                to="articles.templatecategory",
            ),
        ),
    ]
