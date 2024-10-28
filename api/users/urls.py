from django.urls import path

from . import views

urlpatterns = [
    path("login", views.UserLoginView.as_view()),
    path("register", views.UserRegisterView.as_view()),
    path("register/<str:referral_code>", views.UserReferralSignupView.as_view()),
    path("validate-token", views.UserTokenValidation.as_view()),
    path("me", views.CheckAuthenticationStatusView.as_view()),
]
