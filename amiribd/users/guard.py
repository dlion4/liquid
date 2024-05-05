from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.urls import reverse_lazy


LOGIN_REDIRECT_URL = reverse_lazy("home")


class AuthenticationGuard:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
