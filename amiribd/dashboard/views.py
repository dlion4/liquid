from django.shortcuts import render
from django.views.generic import TemplateView
from .guard import DashboardGuard
from amiribd.users.actions import build_signup_referral_link
from decimal import Decimal
from amiribd.transactions.models import Transaction
from typing import Any
from django.db.models import QuerySet
from amiribd.invest.models import Plan


# Create your views here.
class DashboardViewMixin(TemplateView):
    template_name = ""
    queryset: QuerySet | None = None

    # @method_decorator(
    #     cache_page(60), name="dispatch"
    # )  # Cache for 1 minute, adjust as needed
    def get_account_total(self, **kwargs):
        try:
            return self.queryset.objects.get(
                pool__profile=self._get_user().profile_user
            ).balance
        except Exception:
            return Decimal("0.00")

    def get_account_locked_amount(self, **kwargs):
        try:
            transaction = Transaction.objects.get(
                profile=self._get_user().profile_user,
                type="DEPOSIT",
                source="Account Registration",
            )
            return Decimal(transaction.paid)
        except Transaction.DoesNotExist:
            return Decimal("0.00")

    def get_account_available_amount(self, **kwargs):
        try:
            return Decimal(self.get_account_total(**kwargs)) - Decimal(
                self.get_account_locked_amount(**kwargs)
            )
        except Exception:
            return Decimal("0.00")

    def get_profile_plans(self):
        return Plan.objects.filter(
            account__pool__profile=self._get_user().profile_user
        ).all()

    def get_context_data(self, **kwargs):
        profile = self._get_user().profile_user
        context = super().get_context_data(**kwargs)
        context["profile"] = profile
        context["link"] = build_signup_referral_link(self.request, profile)
        context["balance"] = self.get_account_total(**kwargs)
        context["locked_amount"] = self.get_account_locked_amount(**kwargs)
        context["available_amount"] = self.get_account_available_amount(**kwargs)
        context["plans"] = self.get_profile_plans(**kwargs)
        return context


class DashboardView(DashboardViewMixin):
    template_name = "account/dashboard/home.html"

    def _get_user(self):
        return self.request.user

    def _referrals(self):
        return self._get_user().referrals.all().count()

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


dashboard = DashboardView.as_view()


class WelcomeView(DashboardGuard, DashboardViewMixin):
    template_name = "account/dashboard/welcome.html"


welcome = WelcomeView.as_view()
