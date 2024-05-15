from typing import Any
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from .forms import EmailLoginForm, EmailSignupForm
from django.shortcuts import render, redirect
from amiribd.users.models import User, Profile
from allauth.account.views import LoginView as AuthLoginView
from django.views.generic import FormView, View
from django.contrib.auth import get_user_model
import sesame.utils
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


class EmailSesemaAuthenticationLinkView:
    email_template = "account/snippets/email/login.html"

    signup_url = reverse_lazy(settings.SIGNUP_URL)

    def send_html_message(self, context: dict):
        html_message = render_to_string(self.email_template, context)
        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject="[Liquid Investment] LOGIN LINK",
            body=plain_message,
            from_email=None,
            to=[context.get("email")],
        )

        message.attach_alternative(html_message, "text/html")

        message.send()

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
        context = {
            "link": link,
            "user": user,
            "email": email,
        }

        self.send_html_message(context)

    # @method_decorator(after_response.enable)
    def email_submitted(self, email):
        user = self.get_user(email)
        if user is None:
            link = reverse("users:signup")
            link = self.request.build_absolute_uri(link)
            self.send_email(link=link, email=email)

        else:
            link = self.create_link(user=user, path="sesame-login")
            self.send_email(user, link)


@after_response.enable
def send_welcome_email(user, template_name, context: dict):
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject="[Liquid Investment] Successfull onboarding",
        body=plain_message,
        from_email=None,
        to=[user.email],
    )

    message.attach_alternative(html_message, "text/html")

    message.send()


class LoginView(EmailSesemaAuthenticationLinkView, AuthenticationGuard, FormView):
    form_class = EmailLoginForm
    template_name = "account/login.html"
    success_url = reverse_lazy("users:success")

    def form_valid(self, form):
        # TODO: email magic link to user.
        self.email_submitted(form.cleaned_data["email"])
        return super().form_valid(form)


class SignupView(EmailSesemaAuthenticationLinkView, AuthenticationGuard, FormView):
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

            login(self.request, user, backend="sesame.backends.ModelBackend")
            # redirect to home page after login
            return super().form_valid(form)


class SuccessAuthenticationView(AuthenticationGuard, TemplateView):

    template_name = "account/email_login_success.html"


class LogoutView(View):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("home")


class ReferralSignupView(
    EmailSesemaAuthenticationLinkView, AuthenticationGuard, TemplateView
):
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
                login(self.request, user, backend="sesame.backends.ModelBackend")
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
