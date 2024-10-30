from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from amiribd.dashboard.views import DashboardViewMixin
from amiribd.invest.forms import AccountEventWithdrawalForm
from amiribd.invest.forms import CancelPlanForm
from amiribd.invest.models import Account
from amiribd.invest.models import Plan
from amiribd.invest.models import PlanType
from amiribd.invest.views import InvestmentSetupView
from amiribd.transactions.models import Transaction
import contextlib

# Create your views here.


class SubscriptionViewMixin(LoginRequiredMixin, DashboardViewMixin):
    queryset = Account


class SubscriptionAccountView(SubscriptionViewMixin):
    template_name = "account/dashboard/v1/subscriptions/home.html"


class SubscriptionListView(SubscriptionViewMixin):
    template_name = "account/dashboard/v1/subscriptions/subscriptions.html"


class SubscriptionPlanView(InvestmentSetupView, SubscriptionViewMixin):
    template_name = "account/dashboard/v1/subscriptions/subscription.html"
    htmx_template_name = "account/dashboard/v1/investment/partials/transactions.html"
    queryset = Account
    plan = Plan
    tarnasaction = Transaction

    def __transactions(self):
        return Transaction.objects.filter(
            profile=self._get_user().profile_user
        ).order_by("-id")

    def get_object(self) -> Plan:
        """
        This function is obverriden as it requires plan slug and id

        In this case the user is authenticated so we dont need the slug
        Cna use the user id
        return self.request.user.profile_user | User
        args:
            # Plan(profile=self.request.user.profile_user)

        """
        plan = get_object_or_404(
            self.plan,
            account__pool__profile=self._get_user().profile_user,
            slug=self.kwargs.get("plan_slug"),
            pk=self.kwargs.get("plan_id"),
        )

        return plan

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["plan"] = self.get_object()
        context["transactions"] = self.__transactions()
        context["withdrawal_form"] = AccountEventWithdrawalForm()
        context["cancel_plan_form"] = CancelPlanForm()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if request.htmx:
            if type_of_transaction := request.GET.get("type_of_transaction"):
                context["transactions"] = Transaction.objects.filter(
                    type=type_of_transaction, profile=self._get_user().profile_user
                ).order_by("-id")
            return render(request, self.htmx_template_name, context)
        return super().get(request, *args, **kwargs)


class PlanPricingView(SubscriptionViewMixin):
    template_name = "account/dashboard/v1/subscriptions/plans.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile_user  # Assuming the user is authenticated
        # Get the plan types associated with the plans in the user's profile
        profile_plans = list(profile.plans.values_list("type__type", flat=True))
        # Get available plan types excluding those already in the user's profile
        available_plan_types = PlanType.objects.exclude(type__in=profile_plans)
        # Add the available plan types to the context
        context["plans_available"] = available_plan_types
        context["profile"] = profile  # Pass the profile if needed in the template

        return context
