from django.urls import include
from django.urls import path

from .views import LinkAuthenticationView
from .views import LoginView
from .views import LogoutView
from .views import ReferralSignupView
from .views import SignupView
from .views import SuccessAuthenticationView
from .views import TokenExpiredSignupView
from .views import UserView
from .views import ValidatedEmailAddressView

app_name = "users"
urlpatterns = [
    path("login/", view=LoginView.as_view(), name="login"),
    path("auth/user/", view=UserView.as_view(), name="user_view"),
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
    path("profile/", include("amiribd.profiles.urls", namespace="profile")),
]
