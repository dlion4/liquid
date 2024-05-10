from django.urls import path, include
from . import views

app_name = "kyc"

urlpatterns = [
    path("kyc/detail/", views.kyc_profile_detail, name="detail"),
    path("kyc/address/", views.kyc_profile_address, name="address"),
    path("kyc/identity/", views.kyc_profile_identify, name="document"),
    path(
        "kyc/done/verification/",
        views.kyc_profile_complete,
        name="complete_verification",
    ),
    path(
        "kyc/htmx/validation/",
        include(
            "amiribd.dashboard.kyc.htmx.urls",
            namespace="kyc-htmx-validation",
        ),
    ),
]
