from django.urls import path

from .views import LoginView, SignupView, SuccessAuthenticationView

app_name = "users"
urlpatterns = [
    path("login/", view=LoginView.as_view(), name="login"),
    path("signup/", view=SignupView.as_view(), name="signup"),
    path("success/", view=SuccessAuthenticationView.as_view(), name="success"),
]
