import contextlib
from typing import Any, Optional
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
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.contrib.auth.models import User as UserObject
from amiribd.tokens.models import AuthToken
import random
from django.contrib import messages
from .models import Profile as ProfileObject
import string
from .utils import BuildMagicLink, expiring_token_generator, PostCleanFormPostViewMixin, generate_referral_code

@after_response.enable
def send_welcome_email(
    user: UserObject | None = None,
    template_name: str = "",
    context: dict[str, Any] = None,
):
    if context is None:
        context = {
            "team":"Earnkraft",
        }
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject=context.get("subject", "[Liquid Investment] Successful onboarding"),
        body=plain_message,
        from_email=None,
        to=[context.get("email", user.email)],
    )

    message.attach_alternative(html_message, "text/html")

    message.send()


class LoginView(
    AuthenticationGuard,
    BuildMagicLink,
    TemplateView):
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
            queryset = User.objects.filter(email=email)
            if queryset.exists():
                user = queryset.first()
                self._one_time_token_authentication_link(user)
                return render(request, self.template_name, {"form": form, "message": "Login link sent to your inbox"})
            return redirect("users:signup")
        return render(request, self.template_name, {"form": form, })

    def _one_time_token_authentication_link(self, user):
        # Generate a one-time use token for the user
        # Create a unique link for the user to log in
        self.__send_login_email(user)

    def __send_login_email(self, user):
        self.send_login_email(user,"account/dashboard/v1/mails/login.html")



    # create the token code



class SignupView(
    AuthenticationGuard,BuildMagicLink, FormView):
    form_class = EmailSignupForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("home")
    def post(self, request:HttpRequest, *args, **kwargs)->HttpResponse|JsonResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form:EmailSignupForm) -> JsonResponse:
        email:str = form.cleaned_data["email"]
        username:str = form.cleaned_data["username"]
        context:dict[str, Any] = {"url":self.success_url}
        try:
            user = User.objects.get(email=email)
            return redirect("users:login")
        except User.DoesNotExist:
            return self._handle_user_does_not_exists_creation_and_mailing(email, username, context)

    def _handle_user_does_not_exists_creation_and_mailing(
        self, email, username, context):
        user = self._handle_newuser_creation(email, username)
        self.send_welcome_email(
            email,"account/dashboard/v1/mails/welcome.html", 
            {"link":self.build_login_link_from_user(self.request, user),"user": user})
        return redirect("users:login")

    def _handle_newuser_creation(self, email:str, username:str|None =None)->UserObject:
        return self._create_user_in_background(email, username)

    def _create_user_in_background(self, email: str, username: str) -> UserObject:
        user =  User.objects.create_user(email=email, username=username)
        profile:Profile = Profile.objects.get(user=user)
        profile.first_name = username
        profile.save()
        profile.referral_code = generate_referral_code(profile.pk)
        profile.save()
        return user


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
                # self.email_submitted(user.email)
                return redirect("users:login")

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
                self.email_submitted(user)
                login(self.request, user)
                return redirect(self.success_url)

        context = {"form": form}
        return render(request, self.template_name, context)
    
    
    def email_submitted(
            self, 
            user, 
            template:Optional[str]="account/dashboard/v1/mails/welcome.html", 
            context:Optional[dict[str, str]]={}
        ):
        send_welcome_email.after_response(
            user,template,
            {"profile": user.profile_user,
             "link": self.request.build_absolute_uri(reverse("users:login")),
             "policies":self.request.build_absolute_uri(reverse("policies")),
             "subject": "Earnkraft Agencies"
             }
        )

class ReferralSignupView(
    BuildMagicLink, FormView):
    form_class = EmailSignupForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("users:login")
    expired_code_template_name = ""


    def dispatch(self, request, *args:Any, **kwargs:dict):
        """
        Override to check if the referral_code if still valid: it expires in 3 days
        """
        code  = kwargs.get("referral_code")
        if not code or not self.validate_referral_code(code):
            return redirect(reverse("users:expired_token", kwargs={"referral_code": code}))
        return super().dispatch(request, *args, **kwargs)

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
            self.form_valid(form, *args, **kwargs)
        context = {"form": form}
        return render(request, self.template_name, context)

    def form_valid(self, form:EmailSignupForm, *args:Any, **kwargs:Any):
        email = form.cleaned_data["email"]
        username = form.cleaned_data["username"]
        try:
            user = User.objects.get(email=email)
            return redirect("users:login")
        except User.DoesNotExist:
            user = self._create_user_if_unavailable(email, username, *args, **kwargs)
            return redirect(self.success_url)

    def _create_user_if_unavailable(
        self, email: str, username: str,*args:Any, **kwargs:Any,
        ) -> UserObject:
        """
        Creates a new user in the background with the given email,username, and first name.
        Args:email (str): The email address of the user.username (str): The username of the user.
        Returns:UserObject: The newly created user object.
        """
        user:UserObject = User.objects.create_user(email=email, username=username)
        user.save()
        profile:ProfileObject = Profile.objects.get(user=user)
        profile.referred_by = self.get_referrer(*args, **kwargs)
        profile.first_name = username
        profile.save()
        profile.referral_code = generate_referral_code(profile.pk)
        profile.save()
        self.send_welcome_email(email=user.email)
        return user


class TokenExpiredSignupView(TemplateView):
    template_name = "account/expired_token.html"


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

class LinkAuthenticationView(View):
    """
    Invalid test login link:
    http://127.0.0.1:8000/users/login/Mw/ccher2-a4994fd72a57823d4609173f1fc7abbd-sixp32/
    """

    def get(self, request:HttpRequest, uid:Any, token:Any) -> HttpResponse:
        try:
            uuid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uuid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user and expiring_token_generator.check_token(user, token):
            login(request, user, backend="users.backends.TokenAuthenticationBackend")
            return redirect("home")
        # the token is expired show the expired page
        # http://localhost:8000/users/login/Mjk/cazzis-d2df588655e11a203503afe323bf63a9-shg9us/
        messages.error(request, "Your login link is expired!")
        return redirect("users:login")


