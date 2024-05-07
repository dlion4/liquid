from django.shortcuts import render
from django.views.generic import TemplateView
from .guard import DashboardGuard
from amiribd.users.actions import build_signup_referral_link


# Create your views here.
class DashboardViewMixin(TemplateView):
    template_name = ""

    def get_context_data(self, **kwargs):
        profile = self._get_user().profile_user
        context = super().get_context_data(**kwargs)
        context["profile"] = profile
        context["link"] = build_signup_referral_link(self.request, profile)
        return context


class DashboardView(DashboardViewMixin):
    template_name = "account/dashboard/home.html"

    def _get_user(self):
        return self.request.user

    def _referrals(self):
        return self._get_user().referrals.all().count()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plans"] = None
        return context


dashboard = DashboardView.as_view()


class WelcomeView(DashboardGuard, DashboardViewMixin):
    template_name = "account/dashboard/welcome.html"


welcome = WelcomeView.as_view()
