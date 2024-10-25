from django.urls import path

from . import views

urlpatterns = [
    path("login", views.UserLoginView.as_view()),
    path("validate-token", views.UserTokenValidation.as_view()),
]
