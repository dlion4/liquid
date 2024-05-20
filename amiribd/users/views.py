import contextlib
from typing import Any
from django.contrib.auth import authenticate
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from .forms import EmailLoginForm, EmailSignupForm, AuthTokenCodeForm
from django.shortcuts import render, redirect
from amiribd.users.models import User, Profile
from allauth.account.views import LoginView as AuthLoginView
from django.views.generic import FormView, View
from django.contrib.auth import get_user_model
import sesame.utils
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .guard import AuthenticationGuard
import after_response
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.contrib.auth.models import User as UserObject
from amiribd.tokens.models import AuthToken
import random
import string


@after_response.enable
def send_welcome_email(
    user: UserObject | None = None,
    template_name: str = "",
    context: dict[str, Any] = None,
):
    if context is None:
        context = {}
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject=context.get("subject", "[Liquid Investment] Successfull onboarding"),
        body=plain_message,
        from_email=None,
        to=[context.get("email", user.email)],
    )

    message.attach_alternative(html_message, "text/html")

    message.send()


class LoginView(AuthenticationGuard, TemplateView):
    form_class = EmailLoginForm
    template_name = "account/login.html"
    success_url = reverse_lazy("users:success")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if user := User.objects.get(email=email):
                self._extracted_from_post_8(user, request, email)
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})

    def _extracted_from_post_8(self, user, request, email):
        # Generate a one-time use token for the user
        # Create a unique link for the user to log in
        self.send_login_email(user)

    def send_login_email(self, user):

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        link = self.request.build_absolute_uri(f"/users/login/{uid}/{token}/")

        send_welcome_email.after_response(
            user,
            "account/dashboard/v1/mails/login.html",
            {"user": user, "link": link, "subject": "[Liquid Investment]"},
        )


def generate_code(user, length=4):
    code = "".join(random.choice(string.digits) for _ in range(length))
    return AuthToken.objects.create(user=user, code=code, is_active=True)

    # create the token code


class SignupView(AuthenticationGuard, FormView):
    form_class = EmailSignupForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        username = form.cleaned_data["username"]
        # TODO: email magic link to user.
        try:
            user = User.objects.get(email=email)
            self.email_submitted(user.email)
            return redirect("users:success")

        except User.DoesNotExist:
            user = User.objects.create_user(email=email, username=username)
            user.save()
            # create profile after successful user creation
            # profle = Profile.objects.create(user=user)
            # login the user without having to send him/her email

            send_welcome_email.after_response(
                user,
                "account/dashboard/v1/mails/welcome.html",
                {
                    "profile": user.profile_user,
                    "register_url": self.request.build_absolute_uri(
                        reverse("dashboard:invest:invest")
                    ),
                },
            )
            user.backend = "users.backends.TokenAuthenticationBackend"
            login(self.request, user)
            # redirect to home page after login
            return super().form_valid(form)


class SuccessAuthenticationView(AuthenticationGuard, TemplateView):

    template_name = "account/email_login_success.html"
    authToken = AuthToken
    form_class = AuthTokenCodeForm


class LogoutView(View):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("home")


class ReferralSignupView(AuthenticationGuard, TemplateView):
    form_class = EmailSignupForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("home")

    def get_referrer(self, *args, **kwargs):
        return (
            Profile.objects.get(referral_code=referral_code).user
            if (referral_code := kwargs.get("referral_code"))
            else None
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            # TODO: email magic link to user.
            try:
                user = User.objects.get(email=email)
                self.email_submitted(user.email)
                return redirect("users:success")

            except User.DoesNotExist:
                user = User.objects.create_user(email=email, username=username)
                user.save()
                # create profile after successful user creation
                profile = Profile.objects.get(user=user)
                # save the referred by field
                profile.referred_by = self.get_referrer(*args, **kwargs)
                profile.save()
                # redirect to home page after login
                # login the user without having to send him/her email
                send_welcome_email.after_response(
                    user,
                    "account/dashboard/v1/mails/welcome.html",
                    {
                        "profile": profile,
                        "register_url": self.request.build_absolute_uri(
                            reverse("dashboard:invest:invest")
                        ),
                    },
                )
                login(self.request, user)
                return redirect(self.success_url)

        context = {"form": form}
        return render(request, self.template_name, context)


class HtmxSetupView(View):
    html_swap_message = ""

    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


class HandleHtmxEmailLookupView(HtmxSetupView):

    def filter_user(self, request):
        email = request.GET.get("email")
        return User.objects.filter(email=email).first()

    def success_html_response(self, *args, **kwargs):
        self.html_swap_message = """
                <small class='text-muted uk-text-success' id='email-lookup-result'>Email address found</small>
            """

        return self.html_swap_message

    def fail_html_response(self, *args, **kwargs):
        self.html_swap_message = """
            <small class='text-muted uk-text-danger' data-bt-state='disabled' id='email-lookup-result'>No such email address found</small>
        """

        return self.html_swap_message

    def get(self, request, *args, **kwargs):

        if self.filter_user(request):

            return HttpResponse(self.success_html_response(*args, **kwargs))

        return HttpResponse(self.fail_html_response(*args, **kwargs))


class HandleHtmxSignupEmailLookupView(HandleHtmxEmailLookupView):
    def fail_html_response(self, *args, **kwargs):
        self.html_swap_message = """
            <small class='text-muted uk-text-danger' data-bt-state='disabled' id='email-lookup-result'>Email address already taken</small>
        """

        return self.html_swap_message

    def success_html_response(self, *args, **kwargs):
        self.html_swap_message = """
                <small class='text-muted uk-text-success' id='email-lookup-result'></small>
            """

        return self.html_swap_message

    def get(self, request, *args, **kwargs):

        if self.filter_user(request):

            return HttpResponse(self.fail_html_response(*args, **kwargs))

        return HttpResponse(self.success_html_response(*args, **kwargs))


def login_with_link(request, uid, token):
    try:
        uuid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uuid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        # Log the user in without requiring a password
        # user.backend = "users.backends.TokenAuthenticationBackend"
        login(request, user, backend="users.backends.TokenAuthenticationBackend")

        print(user.is_authenticated)

        return redirect("home")  # Replace 'home' with the URL to redirect after login

    print(user.is_authenticated)

    return redirect("users:login")
