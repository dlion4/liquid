from django.urls import path, include

from .views import (
    LoginView,
    SignupView,
    SuccessAuthenticationView,
    LogoutView,
    ReferralSignupView,
    HandleHtmxEmailLookupView,
    HandleHtmxSignupEmailLookupView,
    LinkAuthenticationView,
    TokenExpiredSignupView,
    ValidatedEmailAddressView
)

app_name = "users"
urlpatterns = [
    path("login/", view=LoginView.as_view(), name="login"),
    path("login/<uid>/<token>/", view=LinkAuthenticationView.as_view(), name="login_with_link"),
    path("logout/", view=LogoutView.as_view(), name="logout"),
    path("signup/", view=SignupView.as_view(), name="signup"),
    path("login/validate-email-address", view=ValidatedEmailAddressView.as_view(), name="validate_email_address"),
    path(
        "signup/<str:referral_code>/",
        view=ReferralSignupView.as_view(),
        name="referred-signup",
    ),
    path(
        "token-expired/<str:referral_code>/",
        view=TokenExpiredSignupView.as_view(),
        name="expired_token"),
    path("success/", view=SuccessAuthenticationView.as_view(), name="success"),
    path(
        "htmx-email-lookup/",
        view=HandleHtmxEmailLookupView.as_view(),
        name="email-lookup",
    ),
    path(
        "htmx-signup-email-lookup/",
        view=HandleHtmxSignupEmailLookupView.as_view(),
        name="signup-email-lookup",
    ),
    path("profile/", include("amiribd.profiles.urls", namespace="profile")),
]
