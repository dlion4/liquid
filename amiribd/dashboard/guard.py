from typing import Any
from django import http
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user


class DashboardGuard(LoginRequiredMixin):
    main_dashboard = reverse_lazy(settings.DASHBOARD_URL)

    def _get_user(self):
        return get_user(self.request)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        if request.user.profile_user and request.user.profile_user.kyc_completed:
            return redirect(self.main_dashboard)
        return super().dispatch(request, *args, **kwargs)
