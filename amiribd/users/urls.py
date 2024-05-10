from django.urls import path, include

from .views import (
    LoginView,
    SignupView,
    SuccessAuthenticationView,
    LogoutView,
    ReferralSignupView,
    HandleHtmxEmailLookupView,
    HandleHtmxSignupEmailLookupView
)

app_name = "users"
urlpatterns = [
    path("login/", view=LoginView.as_view(), name="login"),
    path("logout/", view=LogoutView.as_view(), name="logout"),
    path("signup/", view=SignupView.as_view(), name="signup"),
    path(
        "signup/<str:referral_code>/", view=ReferralSignupView.as_view(), name="referred-signup"
    ),
    path("success/", view=SuccessAuthenticationView.as_view(), name="success"),
    path("htmx-email-lookup/", view=HandleHtmxEmailLookupView.as_view(), name="email-lookup"),
    path("htmx-signup-email-lookup/", view=HandleHtmxSignupEmailLookupView.as_view(), name="signup-email-lookup"),

    path("profile/", include("amiribd.profiles.urls", namespace="profile")),
]
