from django.urls import path

from . import views

urlpatterns = [
    path("login", views.UserLoginView.as_view()),
    path("validate-token", views.UserTokenValidation.as_view()),
    path("validate-access-token", views.UserValidateAccessToken.as_view()),
    path("me", views.CheckAuthenticationStatusView.as_view()),
]
