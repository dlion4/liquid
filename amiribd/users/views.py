from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from .forms import EmailLoginForm, EmailSignupForm
from django.shortcuts import render
from amiribd.users.models import User
from allauth.account.views import LoginView as AuthLoginView
from django.views.generic import FormView


class LoginView(FormView):
    form_class = EmailLoginForm
    template_name = "account/login.html"
    success_url = reverse_lazy("users:success")

    def form_valid(self, form):
        # TODO: email magic link to user.
        return super().form_valid(form)


class SignupView(FormView):
    form_class = EmailSignupForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("users:success")

    def form_valid(self, form):
        # TODO: email magic link to user.
        return super().form_valid(form)


class SuccessAuthenticationView(TemplateView):
    template_name = "account/email_login_success.html"
