from django.shortcuts import render
from django.views.generic import TemplateView
from .guard import DashboardGuard
from amiribd.users.actions import build_signup_referral_link
from decimal import Decimal
from amiribd.transactions.models import Transaction
from typing import Any
from django.db.models import QuerySet
from amiribd.invest.models import Plan, Account
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q, F, Sum


# Create your views here.
class DashboardViewMixin(TemplateView):
    template_name = ""
    queryset: QuerySet | None = None

    # @method_decorator(
    #     cache_page(60), name="dispatch"
    # )  # Cache for 1 minute, adjust as needed

    def __pure_referral_earnings(self):
        __referral_profit = Decimal("0.00")
        try:
            account = self.queryset.objects.get(
                pool__profile=self._get_user().profile_user
            )
            __referral_profit = account.transaction_account.filter(
                Q(source__icontains="Referral Earnings")
            ).aggregate(total_paid=Sum("paid"))["total_paid"]
        except Exception as e:
            print(f"Error calculating current date transactions: {e}")
            __referral_profit = Decimal("0.00")

        print("Current Date Profit", __referral_profit)

        return __referral_profit if __referral_profit is not None else Decimal("0.00")

    def __current_date_transaction_profit(self):
        __current_date_profit: Decimal = Decimal("0.00")
        try:
            __current_date = timezone.now() - timedelta(days=1)
            account = self.queryset.objects.get(
                pool__profile=self._get_user().profile_user
            )
            __current_date_profit = account.transaction_account.filter(
                Q(source__icontains="Referral Earnings")
                & Q(created_at__gte=__current_date)
            ).aggregate(total_paid=Sum("paid"))["total_paid"]
        except Exception as e:
            print(f"Error calculating current date transactions: {e}")
            __current_date_profit = Decimal("0.00")

        print("Current Date Profit", __current_date_profit)

        return (
            __current_date_profit
            if __current_date_profit is not None
            else Decimal("0.00")
        )

    def __current_month_transactions(self):
        __month_profit: Decimal = Decimal("0.00")
        try:
            last_month = timezone.now() - timedelta(days=30)
            account = self.queryset.objects.get(
                pool__profile=self._get_user().profile_user
            )
            __month_profit = account.transaction_account.filter(
                Q(source__icontains="Referral Earnings") & Q(created_at__gte=last_month)
            ).aggregate(total_paid=Sum("paid"))["total_paid"]
            print(__month_profit)
        except Exception as e:
            print(f"Error calculating current month transactions: {e}")
            __month_profit = Decimal("0.00")

        print("Month Profit", __month_profit)

        return __month_profit if __month_profit is not None else Decimal("0.00")

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

    def get_profile_plans(self, **kwargs):
        return Plan.objects.filter(
            account__pool__profile=self._get_user().profile_user
        ).all()

    def _get_profile_active_plans(self, **kwargs):
        return self.get_profile_plans().filter(status="RUNNING")

    def profile_account(self):
        return (
            Account.objects.filter(pool__profile=self._get_user().profile_user)
            .all()
            .first()
        )

    def get_context_data(self, **kwargs):
        profile = self._get_user().profile_user
        context = super().get_context_data(**kwargs)
        context["profile"] = profile
        context["link"] = build_signup_referral_link(self.request, profile)
        context["balance"] = self.get_account_total(**kwargs)
        context["locked_amount"] = self.get_account_locked_amount(**kwargs)
        context["available_amount"] = self.get_account_available_amount(**kwargs)
        context["plans"] = self.get_profile_plans(**kwargs)
        context["active_plans"] = self._get_profile_active_plans(**kwargs)
        context["account"] = self.profile_account()
        context["monthly_profit"] = self.__current_month_transactions()
        context["daily_profit"] = self.__current_date_transaction_profit()
        context["referral_earnings"] = self.__pure_referral_earnings()
        return context


class DashboardView(DashboardViewMixin):
    template_name = "account/dashboard/home.html"
    queryset = Account

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
