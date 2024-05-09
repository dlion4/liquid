import contextlib
from typing import Any
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import FormView, TemplateView
from django.urls import reverse, reverse_lazy
from django.conf import settings
from .forms import (
    AccountEventWithdrawalForm,
    AddPlanForm,
    CancelPlanForm,
    PoolRegistrationForm,
    AccountRegistrationForm,
    PlanRegistrationForm,
    PaymentOptionForm,
)
from django.db import transaction

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Pool, Account, Plan
from amiribd.dashboard.views import DashboardGuard, DashboardViewMixin
from decimal import Decimal  # Import Decimal from the decimal module
from django.utils.termcolors import colorize
from amiribd.transactions.models import Transaction

# Create your views here.


class InvestmentSetupView(DashboardGuard, TemplateView):
    template_name = ""

    def dispatch(self, request, *args, **kwargs):
        if (
            not Pool.objects.filter(profile=self._get_user().profile_user).exists()
            and request.resolver_match.view_name != "dashboard:invest:invest"
        ):
            return redirect(reverse("dashboard:invest:invest"))
        else:
            return super().dispatch(request, *args, **kwargs)


class InvestmentRegistrationView(InvestmentSetupView):
    form_class = PoolRegistrationForm
    template_name = "account/dashboard/investment/setup.html"
    success_url = reverse_lazy("dashboard:invest:plans")

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["poolform"] = self.form_class()
        context["accountform"] = AccountRegistrationForm()
        context["planform"] = PlanRegistrationForm()
        context["payoptions"] = PaymentOptionForm()
        return context

    # Simplified and optimized version of the post method

    # Simplified and optimized version of the post method
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        poolForm = self.form_class(request.POST)
        accountForm = AccountRegistrationForm(request.POST)
        planForm = PlanRegistrationForm(request.POST)
        payoptions = PaymentOptionForm(request.POST)

        if all(
            form.is_valid() for form in [poolForm, accountForm, planForm, payoptions]
        ):
            poolInstance = poolForm.save(commit=False)
            poolInstance.profile = self._get_user().profile_user
            poolInstance.save()
            poolForm.save()
            # poolInstance.refresh_from_db()

            accountInstance = accountForm.save(commit=False)
            accountInstance.pool = poolInstance
            accountInstance.save()
            accountForm.save()
            # accountInstance.refresh_from_db()

            planInstance = planForm.save(commit=False)
            planInstance.account = accountInstance
            planInstance.save()
            planForm.save()
            # planInstance.refresh_from_db()

            totalInvestment = sum(
                instance.type.price
                for instance in [poolInstance, accountInstance, planInstance]
            )
            print(totalInvestment, "Total Investment")
            discountPrice = Decimal(Decimal("0.3") * Decimal(totalInvestment))
            print(discountPrice, "Discount Price")
            paymentChannel = payoptions.cleaned_data.get("channel")

            print(paymentChannel, "Channel")

            planInstance.payment_method = paymentChannel.channel
            planInstance.save()

            transaction = Transaction.objects.create(
                profile=poolInstance.profile,
                account=accountInstance,
                type="DEPOSIT",
                amount=totalInvestment,
                discount=discountPrice,
                source="Account Registration",
            )

            print(transaction.paid, "paid amount|Deposited")

            accountInstance.balance = Decimal(
                Decimal(accountInstance.balance) + Decimal(transaction.paid)
            )
            accountInstance.save()

            # look for the referrer
            print(accountInstance.balance, "Account Balance")

            profile = poolInstance.profile

            with contextlib.suppress(Exception):
                if referrer := profile.referred_by:
                    print(
                        referrer,
                        "User",
                        referrer.profile_user,
                        "Profile ser",
                        profile,
                        "Profile thats onbording",
                    )

                    # update the referrer account by a percentage of the deposit
                    referrer_profile = referrer.profile_user
                    referrer_profile_account = Account.objects.get(
                        pool__profile=referrer_profile
                    )
                    interest_earned = Decimal(
                        Decimal("0.35") * Decimal(transaction.paid)
                    )
                    print(interest_earned, "Interest to be earned")

                    transaction = Transaction.objects.create(
                        profile=referrer_profile,
                        account=referrer_profile_account,
                        type="DEPOSIT",
                        amount=interest_earned,
                        discount=Decimal("0.00"),
                        source="Referral Earnings",
                    )
                    transaction.save()
                    referrer_profile_account.balance += transaction.paid
                    # referrer_profile_account.interest +=
                    # now save the transaction
                    referrer_profile_account.save()
                    # referrer_profile_account.refresh_from_db()

                    print(
                        referrer_profile_account.balance, "Account balance of refferer"
                    )

                    # lets create a transaction record for this transaction

            return redirect(self.success_url)

        for form in [poolForm, accountForm, planForm, payoptions]:
            if form.errors:
                for choice in form.fields["type"].choices:
                    print(choice)
                print(form.errors)

        return render(
            request,
            self.template_name,
            {
                "poolform": poolForm,
                "accountform": accountForm,
                "planform": planForm,
                "payoptions": payoptions,
            },
        )


invest = InvestmentRegistrationView.as_view()


class InvestmentSchemeView(InvestmentSetupView, DashboardViewMixin):
    template_name = "account/dashboard/investment/plans.html"
    queryset = Account

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["withdrawal_form"] = AccountEventWithdrawalForm()
        context["add_plan_form"] = AddPlanForm()
        return context


plans = InvestmentSchemeView.as_view()


class InvestmentPlanView(InvestmentSetupView, DashboardViewMixin):
    template_name = "account/dashboard/investment/plan.html"
    queryset = Account
    plan = Plan
    tarnasaction = Transaction

    def __transactions(self):
        return Transaction.objects.filter(
            profile=self._get_user().profile_user
        ).order_by("-id")

    def get_object(self):
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


plan = InvestmentPlanView.as_view()
