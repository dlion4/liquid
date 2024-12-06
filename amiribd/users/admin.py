# for handling aws file download requests
import time

from boto3.session import Session
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _
from unfold import admin as unfold_admin
from unfold.admin import ModelAdmin

from amiribd.core.admin import earnkraft_site
from amiribd.liquid.actions import send_email_to_user
from amiribd.profilesettings.models import NotificationSubscription

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import Address
from .models import Document
from .models import Profile
from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin, ModelAdmin):
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
    list_display = ["email", "name","is_staff", "is_superuser"]
    search_fields = ["name"]
    ordering = ["-id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    readonly_fields = ["date_joined"]
    actions = ["send_payment_email","send_application_email","send_task_email"]
    @admin.action(description="Send Payment Email")
    def send_payment_email(self, request, queryset):
        for user in queryset:
            time.sleep(2)
            send_email_to_user(
                self,
                request,
                recipient=user,
                mail_group="Payment",
                template="liquid/mails/payment.html",
            )

    @admin.action(description="Send Application Email")
    def send_application_email(self, request, queryset):
        for user in queryset:
            time.sleep(2)
            send_email_to_user(
                self,
                request,
                recipient=user,
                mail_group="Application",
                template="liquid/mails/application.html",
            )

    @admin.action(description="Send Task Response Email")
    def send_task_email(self, request, queryset):
        for user in queryset:
            time.sleep(2)
            send_email_to_user(
                self,
                request,
                recipient=user,
                mail_group="Task",
                template="liquid/mails/task.html",
            )

class NotificationSubscriptionInline(unfold_admin.TabularInline):
    model = NotificationSubscription
    extra = 0


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
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
        "referrals",
    )
    list_editable = [
        "is_document_set",
        "is_address_set",
        "kyc_completed",
        "kyc_validated",
    ]
    search_fields = ("user",)
    ordering = ("-id",)
    inlines = [NotificationSubscriptionInline]


@admin.register(Address, site=earnkraft_site)
class AddressAdmin(ModelAdmin):
    list_display = [
        "profile",
        "addr_line1",
        "addr_line2",
        "city",
        "state",
        "country",
        "zip_code",
    ]


session = Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
)

s3_files_resource = session.resource("s3")

s3_bucket_name = settings.AWS_STORAGE_BUCKET_NAME

s3_project_bucket_name = s3_files_resource.Bucket(s3_bucket_name)


@admin.register(Document, site=earnkraft_site)
class DocumentAdmin(ModelAdmin):
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

    actions = [
        "download_kyc_document",
    ]


    @admin.action(description="Download Document")
    def download_kyc_document(self, request, queryset):
        s3_p_files = s3_project_bucket_name.objects.all()  # noqa: F841
        for _doc in queryset:
            """
            TODO: ::
                    implement the code block later
            """
