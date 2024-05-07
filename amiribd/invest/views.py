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
            poolInstance.refresh_from_db()

            accountInstance = accountForm.save(commit=False)
            accountInstance.pool = poolInstance
            accountInstance.save()
            accountForm.save()
            accountInstance.refresh_from_db()

            planInstance = planForm.save(commit=False)
            planInstance.account = accountInstance
            planInstance.save()
            planForm.save()
            planInstance.refresh_from_db()

            totalInvestment = sum(
                instance.type.price
                for instance in [poolInstance, accountInstance, planInstance]
            )
            amountTobePaid = Decimal("0.3") * totalInvestment
            amountTobePaid = Decimal(amountTobePaid)

            paymentChannel = payoptions.cleaned_data.get("channel")

            print(amountTobePaid)
            print(paymentChannel)

            transaction = Transaction.objects.create(
                profile=poolInstance.profile,
                account=accountInstance,
                type="DEPOSIT",
                amount=totalInvestment,
                discount=amountTobePaid,
                source="Account Registration",
            )

            print(transaction)

            accountInstance.balance = transaction.paid
            accountInstance.save()

            return redirect(self.success_url)

        print(form.errors for form in [poolForm, accountForm, planForm, payoptions])

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


class InvestmentPlanView(DashboardGuard, TemplateView):
    template_name = "account/dashboard/investment/plans.html"
    queryset = Account

    def dispatch(self, request, *args, **kwargs):
        if not Pool.objects.filter(profile=self._get_user().profile_user).exists():
            return redirect("dashboard:invest:invest")
        return super().dispatch(request, *args, **kwargs)

    # @method_decorator(
    #     cache_page(60), name="dispatch"
    # )  # Cache for 1 minute, adjust as needed
    def get_account_total(self, **kwargs):
        balance = self.queryset.objects.get(
            pool__profile=self._get_user().profile_user
        ).balance

        # print(balance)
        return balance

    def get_account_locked_amount(self, **kwargs):
        transaction = Transaction.objects.get(
            profile=self._get_user().profile_user,
            type="DEPOSIT",
            source="Account Registration",
        )
        return transaction.paid
        # return Decimal(
        #     Decimal(self.get_account_total(**kwargs)) - Decimal(transaction.paid)
        # )

    def get_account_available_amount(self, **kwargs):
        return Decimal(
            Decimal(self.get_account_total(**kwargs))
            - Decimal(self.get_account_locked_amount(**kwargs))
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["balance"] = self.get_account_total(**kwargs)
        context["locked_amount"] = self.get_account_locked_amount(**kwargs)
        context["available_amount"] = self.get_account_available_amount(**kwargs)
        return context


plans = InvestmentPlanView.as_view()
