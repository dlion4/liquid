# Generated by Django 5.0.4 on 2024-05-05 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0012_alter_profile_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="kyc_completed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="profile",
            name="kyc_completed_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="date_joined",
            field=models.DateField(auto_now_add=True),
        ),
    ]
