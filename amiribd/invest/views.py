import contextlib
from typing import Any
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView
from django.urls import reverse, reverse_lazy
from django.conf import settings
from .forms import (
    PoolRegistrationForm,
    AccountRegistrationForm,
    PlanRegistrationForm,
    PaymentOptionForm,
)
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Pool, Account
from amiribd.dashboard.views import DashboardGuard, DashboardViewMixin
from decimal import Decimal  # Import Decimal from the decimal module

from amiribd.transactions.models import Transaction

# Create your views here.


class InvestmentRegistrationView(DashboardGuard, TemplateView):
    form_class = PoolRegistrationForm
    template_name = "account/dashboard/investment/setup.html"
    success_url = reverse_lazy("dashboard:invest:plans")

    def dispatch(self, request, *args, **kwargs):
        if Pool.objects.filter(profile=self._get_user().profile_user).exists():
            return redirect("dashboard:invest:plans")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["poolform"] = self.form_class()
        context["accountform"] = AccountRegistrationForm()
        context["planform"] = PlanRegistrationForm()
        context["payoptions"] = PaymentOptionForm()
        return context

    # Simplified and optimized version of the post method

    # Simplified and optimized version of the post method
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
            print(totalInvestment)
            discountPrice = Decimal(Decimal("0.3") * Decimal(totalInvestment))
            print(discountPrice)
            paymentChannel = payoptions.cleaned_data.get("channel")

            print(paymentChannel)

            transaction = Transaction.objects.create(
                profile=poolInstance.profile,
                account=accountInstance,
                type="DEPOSIT",
                amount=totalInvestment,
                discount=discountPrice,
                source="Account Registration",
            )

            print(transaction.paid)

            accountInstance.balance = Decimal(
                Decimal(accountInstance.balance) + Decimal(transaction.paid)
            )
            accountInstance.save()

            # look for the referrer

            profile = poolInstance.profile

            with contextlib.suppress(Exception):
                if referrer := profile.referred_by:
                    print(referrer)

                    # update the referrer account by a percentage of the deposit
                    referrer_profile = referrer.profile_user
                    referrer_profile_account = Account.objects.get(
                        pool__profile=referrer_profile
                    )
                    interest_earned = Decimal(
                        Decimal("0.35") * Decimal(transaction.paid)
                    )
                    print(interest_earned)
                    
                    transaction = Transaction.objects.create(
                        profile=profile,
                        account=referrer_profile_account,
                        type="DEPOSIT",
                        amount=interest_earned,
                        discount=Decimal("0.00"),
                        source=f"Referral Earnings from {profile}",
                    )

                    referrer_profile_account.balance = (
                        interest_earned + referrer_profile_account.balance
                    )
                    # now save the transaction
                    referrer_profile_account.save()
                    # referrer_profile_account.refresh_from_db()

                    print(referrer_profile_account)

                    # lets create a transaction record for this transaction


                    transaction.save()

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


class InvestmentPlanView(DashboardGuard, DashboardViewMixin):
    template_name = "account/dashboard/investment/plans.html"
    queryset = Account

    def dispatch(self, request, *args, **kwargs):
        if not Pool.objects.filter(profile=self._get_user().profile_user).exists():
            return redirect("dashboard:invest:invest")
        return super().dispatch(request, *args, **kwargs)


plans = InvestmentPlanView.as_view()
