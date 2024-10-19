import json
from typing import Any

import after_response
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User as UserObject
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import View

from amiribd.tokens.models import AuthToken
from amiribd.users.models import Profile
from amiribd.users.models import User

from .forms import AuthTokenCodeForm
from .forms import EmailLoginForm
from .forms import EmailSignupForm
from .guard import AuthenticationGuard
from .models import Profile as ProfileObject
from .tasks import send_background_email
from .utils import BuildMagicLink
from .utils import expiring_token_generator
from .utils import generate_referral_code


@after_response.enable
def send_welcome_email(
    user: UserObject | None = None,
    template_name: str = "",
    context: dict[str, Any] | None = None,
):
    if context is None:
        context = {"team":"Earnkraft"}
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    context["subject"] = context.get("subject", "[Liquid Investment] Successful onboarding")
    send_background_email(user, template_name, context, [context.get("email", user.email)])


class LoginView(AuthenticationGuard,BuildMagicLink,TemplateView):
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
                self.send_login_email(user, "account/dashboard/v1/mails/login.html")
                return JsonResponse(
                    {"message": "Login link sent to your email"}, status=200)
            return JsonResponse(
                {"errors": json.dumps(["Invalid email address", "Unregistered user"])}, status=400
            )
        return JsonResponse({"errors": json.dumps(form.errors.as_json())}, status=400)


class SignupView(AuthenticationGuard,BuildMagicLink, FormView):
    """
    """
    form_class = EmailSignupForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("home")

    def post(self, request:HttpRequest, *args, **kwargs) -> HttpResponse|JsonResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            if response := self.validate_email_address(
                email_address=form.cleaned_data["email"],
            ):
                return self.form_valid(form)
            return JsonResponse(
                {"message": "Could not validate email address"}, status=400)
        return render(request, self.template_name, {"form": form})

    def form_valid(self, form:EmailSignupForm) -> JsonResponse:
        email:str = form.cleaned_data["email"]
        username:str = form.cleaned_data["username"]
        context:dict[str, Any] = {"url":self.success_url}
        try:
            if user := User.objects.get(email=email):
                return JsonResponse({
                    "url": str(reverse("users:login")),
                    "message": "Email or username already taken",
                })
        except User.DoesNotExist:
            return self._handle_user_does_not_exists_creation_and_mailing(
                email, username, context)

    def _handle_user_does_not_exists_creation_and_mailing(
        self, email, username, context):
        user = self._create_user_in_background(email, username)
        self.send_welcome_email(
            email,"account/dashboard/v1/mails/welcome.html",
            {"link":self.build_login_link_from_user(self.request, user),"user": user})
        return JsonResponse({"url": str(reverse("users:login"))})

    def _create_user_in_background(self, email: str, username: str) -> UserObject|None:
        user =  User.objects.create_user(email=email, username=username)
        profile:Profile = Profile.objects.get(user=user)
        profile.first_name = username
        profile.save()
        profile.referral_code = generate_referral_code(profile.pk)
        profile.save()
        return user


class SuccessAuthenticationView(AuthenticationGuard, TemplateView):

    template_name = "account/email_login_success.html"
    auth_token = AuthToken
    form_class = AuthTokenCodeForm


class LogoutView(View):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("home")

class ReferralSignupView(AuthenticationGuard, BuildMagicLink, FormView):
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
            return redirect(reverse(
                "users:expired_token", kwargs={"referral_code": code}))
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
            if not self.validate_email_address(email_address=email):
                messages.error("Invalid or undeliverable email address")
                if referer := self.request.META.get("HTTP_REFERER"):
                    return redirect(referer)
                return redirect(reverse("users:referred-signup", kwargs={
                    "referral_code":kwargs.get("referral_code"),
                }))
            user = self._create_user_if_unavailable(email, username, *args, **kwargs)
            return JsonResponse({"url": str(reverse(self.success_url))})

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


class ValidatedEmailAddressView(View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get("email")
        # validated = ValidatedEmailAddress.objects.using("email_validation").filter(email_address=email)  # noqa: E501, ERA001
        # if validated.exists():
        # return JsonResponse({"message": "Can't find such an account!", "is_valid": False})  # noqa: E501, ERA001
        return JsonResponse({"message": "Your account exist. 🔥", "is_valid": True}, status=200)
