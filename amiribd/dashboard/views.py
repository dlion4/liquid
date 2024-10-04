from datetime import datetime
from datetime import timedelta
from decimal import Decimal
from itertools import groupby
from typing import Any

from django.db import models
from django.db.models import Count
from django.db.models import Q
from django.db.models import QuerySet
from django.db.models import Sum
from django.utils import timezone
from django.utils.timezone import localtime
from django.views.generic import TemplateView

from amiribd.invest.models import Account
from amiribd.invest.models import Plan
from amiribd.schemes.models import WhatsAppEarningScheme
from amiribd.streams.models import Message
from amiribd.streams.models import Post as NotificationPosts
from amiribd.streams.models import Room
from amiribd.streams.models import RoomMessage
from amiribd.transactions.models import Transaction
from amiribd.users.actions import build_signup_referral_link

from .guard import DashboardGuard


# Create your views here.
class DashboardViewMixin(TemplateView):
    template_name = ""
    queryset: QuerySet | None = None

    # @method_decorator(
    #     cache_page(60), name="dispatch"
    # )  # Cache for 1 minute, adjust as needed
    def __get_user(self):
        return self.request.user

    def get_profile(self):
        """
        Retrieves the user's profile.
        Returns:
        Profile: The user's profile.
        """
        return self.__get_user().profile_user

    def get_total_whatsapp_earnings(self):
        """
        Calculates the total earnings from WhatsApp views and prices.

        Parameters:
        self (DashboardViewMixin): The instance of the class.
        Returns:
        Decimal: The total earnings from WhatsApp views and prices.
        If no earnings are found, returns 0.00.
        """
        earnings = (
            WhatsAppEarningScheme.objects.prefetch_related("profile")
            .filter(profile=self.get_profile(), approved=True)
            .aggregate(total=Sum(models.F("views") * models.F("price")))
        )

        if earnings["total"]:
            return Decimal(earnings["total"])
        return Decimal("0.00")

    def __pure_referral_earnings(self):
        __referral_profit = Decimal("0.00")
        try:
            account = self.queryset.objects.get(
                pool__profile=self.__get_user().profile_user,
            )
            __referral_profit = account.transaction_account.filter(
                Q(source__icontains="Referral Earnings"),
            ).aggregate(total_paid=Sum("paid"))["total_paid"]
        except Exception as e:  # noqa: BLE001, F841
            __referral_profit = Decimal("0.00")

        return __referral_profit if __referral_profit is not None else Decimal("0.00")

    def __current_date_transaction_profit(self):
        return self.__extracted_from___current_month_transactions_2(1)

    def __current_month_transactions(self):
        """
         - Rename this here and in `
         __current_date_transaction_profit` and `__current_month_transactions`
        """
        return self.__extracted_from___current_month_transactions_2(30)

    def __extracted_from___current_month_transactions_2(self, days)->Decimal:
        __current_date_profit: Decimal = Decimal("0.00")
        try:
            __current_date = timezone.now() - timedelta(days=days)
            account = self.queryset.objects.get(
                pool__profile=self.__get_user().profile_user,
            )
            __current_date_profit = account.transaction_account.filter(
                    Q(source__icontains="Referral Earnings")
                    & Q(created_at__gte=__current_date),
            ).aggregate(total_paid=Sum("paid"))["total_paid"]
        except Exception as e:  # noqa: BLE001, F841
            __current_date_profit = Decimal("0.00")
        return (
            __current_date_profit
            if __current_date_profit is not None
            else Decimal("0.00")
        )

    def get_account_total(self, **kwargs)->Decimal:
        """
            This function retrieves the total balance of the user's account.

            ### Parameters:
                - kwargs (dict): Additional keyword arguments that
                may be used in future extensions.
            ###   Returns:
                - Decimal: The total balance of the user's account.
                If the account does not exist or an error occurs, it returns 0.00.
        """
        try:
            return self.queryset.objects.get(
                pool__profile=self.__get_user().profile_user,
            ).balance
        except Exception:  # noqa: BLE001
            return Decimal("0.00")


    def get_monthly_site_investments(self):
        """
        This will return the current month's transaction and compare
        it with the previous month's deposit transaction
        and then calculate the percentage gain or loss and display it.
        """
        current_month_start = datetime.now(tz=None).replace(day=1)
        previous_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
        previous_month_end = current_month_start - timedelta(days=1)

        current_month_deposits = self._get_monthly_deposits(current_month_start)
        previous_month_deposits = self._get_monthly_deposits(
            previous_month_start, previous_month_end)

        if previous_month_deposits == 0:
            percentage_change = 0
        else:
            percentage_change = (
                f"{((
                    (current_month_deposits - previous_month_deposits)
                    / previous_month_deposits) * 100):.2f}",
            )
        return {
            "current_month_deposits": current_month_deposits,
            "previous_month_deposits": previous_month_deposits,
            "percentage_change": percentage_change,
        }

    def _get_monthly_deposits(self, start_date, end_date=None):
        """
        This method will return transactions made withing a specific duration of time

        For example between the start and end or april->
        """
        if end_date is None:
            end_date = datetime.now(tz=None)
        return Transaction.objects.filter(
            type="DEPOSIT",
            created_at__gte=start_date,
            created_at__lt=end_date,
        ).prefetch_related(
            "profile").prefetch_related(
                "account").aggregate(
                    total_deposits=Sum("paid"))["total_deposits"] or 0


    def get_account_locked_amount(self, **kwargs):
        try:
            if transaction := Transaction.objects.filter(
                profile=self.__get_user().profile_user,
                type="DEPOSIT",
                source="Account Registration",
            ).aggregate(total=Sum("paid")):
                if transaction["total"] is not None:
                    return Decimal(transaction["total"])
            return Decimal("0.00")
        except Transaction.DoesNotExist:
            return Decimal("0.00")

    def get_account_available_amount(self, **kwargs):
        try:
            return Decimal(self.get_account_total(**kwargs)) - Decimal(
                self.get_account_locked_amount(**kwargs),
            )
        except Exception:  # noqa: BLE001
            return Decimal("0.00")

    def get_profile_plans(self, **kwargs):
        return self.__get_user().profile_user.plans.filter(is_paid=True)

    def _get_profile_active_plans(self, **kwargs):
        return self.get_profile_plans().filter(status="RUNNING")

    def _get_profile_inactive_plans(self, **kwargs):
        return self.get_profile_plans().filter(status="CANCELLED")

    def profile_account(self):
        return (
            Account.objects.filter(pool__profile=self.__get_user().profile_user)
            .all()
            .first()
        )

    def get_account_transactions(self)->Transaction:
        """
        Return the transactions
        made by the logged in user
        """
        return Transaction.objects.filter(
            profile=self.__get_user().profile_user).all()

    def get_total_site_investment(self)->Decimal:
        """
        This function will help in the retrieval of the total amount
        deposited into this site

        It takes the Transaction and then sum together all the amount that has been paid

        :TODO: In most cases will need a model to keep
        transaction of all the amount paid and those withdrawn

        For now just use the account |Transaction

            args eg.::
                    Transaction.objects.filter(type="Deposit").aggregate(investments=Sum("paid"))['investment']
                -> Optional: can filter for the account registration or not |
                IN this case it has been ignored
                -> Decimal(0.00) + Decimal(self.get_total_whatsapp_earnings())
                -> Decimal(0.00) + Decimal(self.get_total_site_investment())
        """
        investments =  Transaction.objects.filter(
            type="DEPOSIT").prefetch_related(
                "profile").aggregate(investments=Sum("paid"))["investments"]
        if investments is None:
            return Decimal("0.00")
        return Decimal(investments)

    def get_total_paid_profit(self)->Decimal:
        """
        This function will help in the retrieval of the total paid profit
        from the referral earnings
        :TODO:
        In most cases will need a model to keep transaction of all
        the amount paid and those withdrawn

        For now just use the account |Transaction
        """
        profits =  Transaction.objects.filter(
            source__icontains="Referral Earnings").prefetch_related(
                "profile").prefetch_related("account").aggregate(profits=Sum("paid"))["profits"]
        return Decimal(profits) if profits is not None else Decimal("0.00")

    def __premium_user(self):
        return self.request.user.groups.filter(name="Premium").exists()

    def site_plan_population(self):
        """
        ### Query all instances of YourModelName that have associated plans
        This returns the plan population and polarity
         PlanType.objects.prefetch_related("account").filter()
         -  look for plan that have the plan type and count them and they should not be
         duplicate
         -  example i have 3 plan type basic, standard and gold,  many users can have
         basic plan but the type is one
         -  so i need the plan total per plan type
         -  the also find which user have plan
         -  that have basic plan and have only one basic plan
         -  the same for standard and gold
         -  profiles_with_plans = Profile.objects.filter(plans__isnull=False)
         -  total_profile_in_the_website = Profile.objects.all()
        """

        plan_counts = Plan.objects.values(
            "type__type").annotate(total_plans=Count("id", distinct=True))
        # Calculate total sum of plans
        total_sum_plans = sum(item["total_plans"] for item in plan_counts)



        # Calculate percentage of total for each PlanType
        for plan in plan_counts:
            plan["percentage_of_total"] = (
                f"{((plan['total_plans'] / total_sum_plans) * 100):.0f}"
                if total_sum_plans != 0 else 0
            )

        return plan_counts


    def get_context_data(self, **kwargs)->dict[str,Any]:
        """
        Calls super().get_context_data(**kwargs) to get the base context.
        Updates the context with data from the helper methods:
        get_profile_context, get_account_context, get_plans_context,
        get_transactions_context, and get_earnings_context.
        """
        context = super().get_context_data(**kwargs)
        context.update(self.get_profile_context())
        context.update(self.get_account_context(**kwargs))
        context.update(self.get_plans_context(**kwargs))
        context.update(self.get_transactions_context())
        context.update(self.get_earnings_context())
        context.update(self.get_notifications_context())
        context["monthly_site_investments"] = self.get_monthly_site_investments()
        return context

    def get_profile_context(self)->dict[str, Any]:
        """
            Gathers profile-related data such as the user profile,
            referral link, account, and premium status.
            :return: A dictionary with profile-related data.
            :rtype: dict
        """
        profile = self.__get_user().profile_user
        return {
            "profile": profile,
            "link": build_signup_referral_link(self.request, profile),
            "account": self.profile_account(),
            "is_premium": self.__premium_user(),
        }

    def get_account_context(self, **kwargs):
        """"
        Gathers account-related data such as balance, locked amount,
        available amount, total site deposit, and total paid profits.
        :return: A dictionary with account-related data.
        """
        return {
            "balance": self.get_account_total(**kwargs),
            "locked_amount": self.get_account_locked_amount(**kwargs),
            "available_amount": self.get_account_available_amount(**kwargs),
            "total_site_deposit": self.get_total_site_investment(),
            "total_paid_profits": self.get_total_paid_profit(),
        }

    def get_plans_context(self, **kwargs):
        """
        Gathers plan-related data such as all plans, active plans, and inactive plans.
        """
        return {
            "plans": self.get_profile_plans(**kwargs),
            "active_plans": self._get_profile_active_plans(**kwargs),
            "inactive_plans": self._get_profile_inactive_plans(**kwargs),
            "plans_popularity":self.site_plan_population(),
        }

    def get_transactions_context(self):
        """"
        Gathers transaction-related data such as transactions,
        monthly profit, and daily profit.
        """
        return {
            "transactions": self.get_account_transactions(),
            "monthly_profit": self.__current_month_transactions(),
            "daily_profit": self.__current_date_transaction_profit(),
        }

    def get_earnings_context(self):
        return {
            "referral_earnings": self.__pure_referral_earnings(),
            "earnings": self.get_total_whatsapp_earnings(),
        }
    def get_notifications_context(self):
        return {
            "notifications": NotificationPosts.objects.filter(is_active=True),
        }

class DashboardView(DashboardViewMixin):
    template_name = "account/dashboard/home.html"
    queryset = Account

    def __get_user(self):
        return self.request.user

    def _referrals(self):
        return self.__get_user().referrals.all().count()

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


dashboard = DashboardView.as_view()


class WelcomeView(DashboardGuard, DashboardViewMixin):
    template_name = "account/dashboard/welcome.html"


welcome = WelcomeView.as_view()


class SupportView(DashboardViewMixin):
    template_name = "account/dashboard/v1/support.html"
    queryset = Account

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rooms"] = Room.objects.all()[:5]
        context["collection_messages"] = self.__collection_messages(**kwargs)
        context["my_messages"] = self.__my_messages(**kwargs)
        context["my_referrals"] = self.__my_referrals(**kwargs)
        return context

    def __my_referrals(self, **kwargs):
        return self.request.user.referrals

    def __collection_messages(self, **kwargs):
        messages = RoomMessage.objects.all().order_by("-created_at")
        return {
            date: list(items)
            for date, items in groupby(
                messages,
                key=lambda item: localtime(item.created_at).date(),
            )
        }

    def __my_messages(self, **kwargs):
        return Message.objects.filter(
            receiver=self.request.user.profile_user,
        ).prefetch_related("receiver")

support = SupportView.as_view()

class AssistanceView(SupportView):
    template_name = "account/dashboard/v1/assistance.html"
assistance = AssistanceView.as_view()
