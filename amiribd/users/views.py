from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from .forms import EmailLoginForm, EmailSignupForm
from django.shortcuts import render, redirect
from amiribd.users.models import User
from allauth.account.views import LoginView as AuthLoginView
from django.views.generic import FormView, View
from django.contrib.auth import get_user_model
import sesame.utils
from django.core.mail import send_mail
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import after_response


class EmailSesemaAuthenticationLinkView:

    def get_user(self, email):
        """Find the user with this email address."""
        User = get_user_model()
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def create_link(self, user=None, path=None):
        """Create a login link for this user."""
        link = reverse(path)
        link = self.request.build_absolute_uri(link)
        link += sesame.utils.get_query_string(user)
        return link

    def send_email(self, user=None, link=None, email=None):
        """Send an email with this login link to this user."""
        if user:
            user.email_user(
                subject="[Liquid Investment] Log in to our app",
                message=f"""
                    Hello,

                    You requested that we send you a link to log in to our app:

                        {link}

                    Thank you for using django-sesame!
                    """,
            )
        else:
            send_mail(
                subject="[Liquid Investment] Log in to our app",
                message=f"""
                    Hello,

                    You requested that we send you a link to log in to our app:

                        {link}

                    Thank you for using django-sesame!
                    """,
                from_email="invest@liquidinvestment.com",
                recipient_list=[email],
            )

    @method_decorator(after_response.enable)
    def email_submitted(self, email):
        user = self.get_user(email)
        if user is None:
            # Ignore the case when no user is registered with this address.
            # Possible improvement: send an email telling them to register.
            # print("user not found:", email)
            # link = self.create_link(path="users:signup")

            link = reverse("users:signup")
            link = self.request.build_absolute_uri(link)
            print("user not found:", email)
            self.send_email(link=link, email=email)

        else:
            link = self.create_link(user=user, path="sesame-login")
            self.send_email(user, link)


class LoginView(EmailSesemaAuthenticationLinkView, FormView):
    form_class = EmailLoginForm
    template_name = "account/login.html"
    success_url = reverse_lazy("users:success")

    def form_valid(self, form):
        # TODO: email magic link to user.
        self.email_submitted.after_response(form.cleaned_data["email"])
        return super().form_valid(form)


class SignupView(EmailSesemaAuthenticationLinkView, FormView):
    form_class = EmailSignupForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        username = form.cleaned_data["username"]
        # TODO: email magic link to user.
        try:
            user = User.objects.get(email=email)
            self.email_submitted.after_response(user.email)
            return redirect("users:success")

        except User.DoesNotExist:
            user = User.objects.create_user(email=email, username=username)
            user.save()
            # login the user without having to send him/her email
            login(self.request, user, backend="sesame.backends.ModelBackend")
            # redirect to home page after login
            return super().form_valid(form)


class SuccessAuthenticationView(TemplateView):

    template_name = "account/email_login_success.html"


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("home")


class ReferralSignupView(SignupView):
    form_class = EmailSignupForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        # get the referral code from the url
        referral_code = request.GET.get("referral_code")
        # check if the referral code is valid
        if not referral_code:
            # proceed with normal registration

            return redirect("home")
        # attached the registerred user to a inviter
        return render(request, self.template_name)
