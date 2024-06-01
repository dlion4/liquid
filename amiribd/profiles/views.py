from typing import Any
from django import http
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from amiribd.dashboard.views import DashboardViewMixin
from django.views.generic import View
from amiribd.invest.models import Account
from amiribd.profilesettings.forms import NotificationForm
from amiribd.profilesettings.models import (
    Notification,
    NotificationSubscription,
    NotificationType,
)
from amiribd.tokens.models import Token
from amiribd.tokens.serializers import TokenSerializer
from amiribd.users.models import User
from amiribd.users.serializers import UserSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect

# Create your views here.


class ProfileHtmxSetupView(DashboardViewMixin):
    template_name = "account/profile/index.html"
    htmx_template_name = ""
    queryset = Account

    def dispatch(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        if request.user.is_authenticated:
            if self._get_user().verified:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("dashboard:welcome")
        return redirect(reverse_lazy(settings.LOGIN_URL))

    def _get_user(self):
        return self.request.user

    def htmx_get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.htmx_template_name, context)

    def get(self, request, *args, **kwargs):
        if request.htmx:
            return self.htmx_get(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)


class ProfileView(ProfileHtmxSetupView):
    htmx_template_name = "account/profile/components/personal.html"


class ProfileNotificationView(ProfileHtmxSetupView):
    htmx_template_name = "account/profile/partials/notifications.html"

    def get_subscription_profile(self):
        try:
            return NotificationSubscription.objects.get(
                profile=self.request.user.profile_user, is_active=True
            )
        except Exception:
            return None

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["notifications"] = Notification.objects.all()
        context["notifications-form"] = NotificationForm(object_pk=1)
        context["subscription"] = self.get_subscription_profile()
        return context


class ProfileAccountActivityView(ProfileHtmxSetupView):
    htmx_template_name = "account/profile/partials/activity.html"


class ProfileSecuritySettingView(ProfileHtmxSetupView):
    htmx_template_name = "account/profile/partials/security.html"


class ProfileSocialConnectedView(ProfileHtmxSetupView):
    htmx_template_name = "account/profile/partials/social.html"


class ObtainTokenView(View):
    def get(self, request, *args, **kwargs):
        token = Token.objects.filter(user=self.request.user, is_active=True).first()
        return http.JsonResponse(
            {
                "success": True,
                "user": UserSerializer(self.request.user).data,
                "token": TokenSerializer(token).data,
            }
        )


class TokenVerifyView(View):
    @method_decorator(csrf_exempt, csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")
        user = Token.objects.get(token=token).user
        return http.JsonResponse({"user": UserSerializer(user).data})


class RefreshTokenView(View):

    @method_decorator(csrf_exempt, csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = User.objects.get(pk=user_id)
        # Deactivate all active tokens in one query
        Token.objects.filter(user=user, is_active=True).update(is_active=False)

        # Create a new token
        token = Token.objects.create(user=user)
        return http.JsonResponse(
            {
                "success": True,
                "user": UserSerializer(user).data,
                "token": TokenSerializer(token).data,
            }
        )


class TokenRevokeView(View):
    pass
