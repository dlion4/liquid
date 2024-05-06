from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import User, Profile, Address, Document

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.site.login = login_required(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "is_superuser"]
    search_fields = ["name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "referred_by",
        "image",
        "first_name",
        "last_name",
        "full_name",
        "phone_number",
        "date_of_birth",
        "is_address_set",
        "is_document_set",
        "kyc_completed",
        "kyc_validated",
        "kyc_completed_at",
    )
    list_editable = [
        "is_document_set",
        "is_address_set",
        "kyc_completed",
        "kyc_validated",
    ]
    search_fields = ("user",)
    ordering = ("user",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "profile",
        "addr_line1",
        "addr_line2",
        "city",
        "state",
        "country",
        "zip_code",
    ]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        "profile",
        "document_type",
        "document",
        "read_terms",
        "correct_information",
    ]

    readonly_fields = (
        "document",
        "document_type",
    )
