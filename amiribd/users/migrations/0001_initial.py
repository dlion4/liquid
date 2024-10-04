# Generated by Django 5.0.6 on 2024-08-29 07:23

import amiribd.users.managers
import amiribd.users.models
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("adverts", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("invest", "0002_initial"),
        ("jobs", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Name of User"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email address"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="username"
                    ),
                ),
                ("verified", models.BooleanField(default=False)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "pending"),
                            ("COMPLETED", "completed"),
                            ("BLOCKED", "blocked"),
                            ("SUSPENDED", "suspended"),
                        ],
                        default="PENDING",
                        max_length=255,
                    ),
                ),
                ("date_joined", models.DateField(auto_now_add=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", amiribd.users.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
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
                ("first_name", models.CharField(blank=True, max_length=100)),
                ("last_name", models.CharField(blank=True, max_length=100)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="profile_pics"),
                ),
                (
                    "full_name",
                    models.GeneratedField(
                        db_persist=True,
                        expression=amiribd.users.models.ConcatField(
                            "first_name", models.Value(" "), "last_name"
                        ),
                        output_field=models.TextField(),
                    ),
                ),
                ("kyc_completed", models.BooleanField(default=False)),
                ("kyc_validated", models.BooleanField(default=False)),
                ("kyc_completed_at", models.DateTimeField(blank=True, null=True)),
                ("is_address_set", models.BooleanField(default=False)),
                ("is_document_set", models.BooleanField(default=False)),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must start with a digit and be 9 to 15 digits in total.",
                                regex="^[0-9]\\d{8,14}$",
                            )
                        ],
                    ),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("initials", models.CharField(blank=True, default="AB", max_length=2)),
                ("referral_code", models.CharField(blank=True, max_length=200)),
                (
                    "accepted_job_applications",
                    models.ManyToManyField(
                        blank=True,
                        related_name="profile_accepted_job_applications",
                        to="jobs.jobapplication",
                    ),
                ),
                ("adverts", models.ManyToManyField(blank=True, to="adverts.advert")),
                (
                    "job_applications",
                    models.ManyToManyField(
                        blank=True,
                        related_name="profile_job_applications",
                        to="jobs.job",
                    ),
                ),
                ("plans", models.ManyToManyField(blank=True, to="invest.plan")),
                (
                    "referred_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="profile_referred_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Document",
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
                ("document_type", models.CharField(default="NI", max_length=2)),
                (
                    "document",
                    models.ImageField(
                        upload_to=amiribd.users.models.user_directory_path
                    ),
                ),
                ("read_terms", models.BooleanField(default=False)),
                ("correct_information", models.BooleanField(default=False)),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile_document",
                        to="users.profile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Address",
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
                ("addr_line1", models.CharField(max_length=255)),
                ("addr_line2", models.CharField(blank=True, max_length=255)),
                ("city", models.CharField(max_length=255)),
                ("state", models.CharField(max_length=255)),
                ("country", models.CharField(max_length=255)),
                ("zip_code", models.CharField(max_length=255)),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile_address",
                        to="users.profile",
                    ),
                ),
            ],
        ),
    ]
