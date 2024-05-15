import contextlib
import json
from typing import Any
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import FormView, TemplateView
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from intasend import APIService
from amiribd.payments.helpers import MpesaStkPushSetUp
from amiribd.users.models import Profile
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
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import AccountType, PlanType, Pool, Account, Plan, PoolType
from amiribd.dashboard.views import DashboardGuard, DashboardViewMixin
from decimal import Decimal  # Import Decimal from the decimal module
from django.utils.termcolors import colorize
from amiribd.transactions.models import Transaction
from .serializers import AccountSerializer, PlanSerializer, PoolSerializer

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
        context["poolform"] = self.form_class(request=self.request)
        context["accountform"] = AccountRegistrationForm(request=self.request)
        context["planform"] = PlanRegistrationForm(request=self.request)
        return context

    # Simplified and optimized version of the post method

    # Simplified and optimized version of the post method


invest = InvestmentRegistrationView.as_view()


class HandlePoolSelectionView(LoginRequiredMixin, View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        profile = self.request.user.profile_user
        pool_type = get_object_or_404(PoolType, pk=request.GET.get("pool_type_id"))
        message = ""
        pool_data = None

        pool = Pool.objects.filter(profile=profile)

        if pool.exists():
            account = Account.objects.filter(pool__profile=profile)
            if account.exists():
                plan = Plan.objects.filter(account__pool__profile=profile)
                if plan.exists():
                    plan.delete()
                account.delete()
            pool.delete()

        pool = Pool.objects.create(profile=profile, type=pool_type)
        pool_data = PoolSerializer(pool).data

        return JsonResponse({"success": True, "status": 200, "pool": pool_data})


class HandleAccountSelectionView(LoginRequiredMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        profile = request.user.profile_user

        pool = get_object_or_404(Pool, profile=profile, pk=request.GET.get("pool_id"))

        account_type = get_object_or_404(
            AccountType, pk=request.GET.get("account_type_id")
        )

        account_data = None

        account = Account.objects.filter(pool__profile=profile)

        if account.exists():
            plan = Plan.objects.filter(account__pool__profile=profile)
            if plan.exists():
                plan.delete()
            account.delete()

        account = Account.objects.create(pool=pool, type=account_type)

        account_data = AccountSerializer(account).data

        return JsonResponse(
            {
                "success": True,
                "status": 200,
                "message": "message",
                "account": account_data,
            }
        )


class HandlePlanSelectionView(LoginRequiredMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        profile = request.user.profile_user
        account = get_object_or_404(Account, pk=request.GET.get("account_id"))
        plan_type = get_object_or_404(PlanType, pk=request.GET.get("plan_type_id"))

        plan = Plan.objects.filter(account__pool__profile=profile)
        if plan.exists():
            plan.delete()

        plan = Plan.objects.create(account=account, type=plan_type)
        plan_data = PlanSerializer(plan).data

        return JsonResponse(
            {
                "success": True,
                "status": 200,
                "message": "Plan has been selected.",
                "plan": plan_data,
            }
        )


class HandlePaymentCreateTransactionView(LoginRequiredMixin, View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        profile = request.user.profile_user
        data = json.loads(request.body)
        phone_number = data.get("phone_number")
        pool = Pool.objects.get(profile=profile, pk=kwargs.get("pool_id"))
        account = Account.objects.get(
            pool=pool, pool__profile=profile, pk=kwargs.get("account_id")
        )
        plan = Plan.objects.get(
            account=account, account__pool__profile=profile, pk=kwargs.get("plan_id")
        )

        totalInvestment = sum(instance.type.price for instance in [pool, account, plan])

        discountPrice = Decimal(Decimal("0.2") * Decimal(totalInvestment))

        transaction = Transaction.objects.create(
            profile=profile,
            account=account,
            type="DEPOSIT",
            amount=totalInvestment,
            discount=discountPrice,
            source="Account Registration",
            payment_phone=phone_number,
        )

        account.balance = Decimal(Decimal(account.balance) + Decimal(transaction.paid))
        account.save()

        # look for the referrer
        profile = pool.profile

        self.__get_referrer_and_update_account(profile)

        return JsonResponse(
            {"success": True, "url": reverse_lazy("dashboard:invest:plans")}
        )

    def __get_referrer_and_update_account(self, profile):
        if referrer := profile.referred_by:
            # update the referrer account

            referrer_profile = referrer.profile_user
            referrer_profile_account = Account.objects.get(
                pool__profile=referrer_profile
            )
            interest_earned = Decimal(Decimal("0.25") * Decimal(transaction.paid))

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
            referrer_profile_account.save()


def fetch_amount_tobe_paid_plus_discount(request):
    profile = Profile.objects.get(pk=request.GET.get("profile"))
    pool = Pool.objects.get(profile=profile)
    account = Account.objects.get(pool=pool, pool__profile=profile)
    plan = Plan.objects.get(
        account=account, account__pool__profile=profile, pk=request.GET.get("plan_pk")
    )
    totalInvestment = sum(instance.type.price for instance in [pool, account, plan])
    discountPrice = Decimal(Decimal("0.2") * Decimal(totalInvestment))
    amount_to_be_paid = totalInvestment - discountPrice
    return JsonResponse({"amount": amount_to_be_paid})


class HandleRegistrationPaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        service = MpesaStkPushSetUp().mpesa_stk_push_service()
        phone = request.GET.get("phone")
        amount = request.GET.get("amount")
        profile = Profile.objects.get(pk=request.GET.get("profile"))

        response = service.collect.mpesa_stk_push(
            phone_number=str(phone),
            email=str(profile.user.email),
            amount=amount,
            narrative="Package Purchase Payment",
        )

        return JsonResponse(
            {
                "success": True,
                "status": 200,
                "response": response,
            }
        )


def check_payment_status(request):
    service = MpesaStkPushSetUp().mpesa_stk_push_service()
    response = service.collect.status(invoice_id=request.GET.get("invoice_id"))
    print(response)
    return JsonResponse({"success": True, "response": response})


class InvestmentSchemeView(InvestmentSetupView, DashboardViewMixin):
    template_name = "account/dashboard/investment/plans.html"
    queryset = Account

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["withdrawal_form"] = AccountEventWithdrawalForm()
        context["add_plan_form"] = AddPlanForm(request=self.request)
        return context


plans = InvestmentSchemeView.as_view()


class InvestmentPlanView(InvestmentSetupView, DashboardViewMixin):
    template_name = "account/dashboard/investment/plan.html"
    htmx_template_name = "account/dashboard/investment/partials/transactions.html"
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

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if request.htmx:
            if type_of_transaction := request.GET.get("type_of_transaction"):
                print(type_of_transaction)
                context["transactions"] = Transaction.objects.filter(
                    type=type_of_transaction, profile=self._get_user().profile_user
                ).order_by("-id")
            return render(request, self.htmx_template_name, context)
        return super().get(request, *args, **kwargs)


plan = InvestmentPlanView.as_view()

# modified view way of creting views


class WidsthdrawView(TemplateView):
    template_name = "account/dashboard/investment/withdrawal.html"


modified_widthdrawal_view = WidsthdrawView.as_view()


class WalletView(TemplateView):
    template_name = "account/dashboard/investment/wallet.html"


modified_wallet_view = WalletView.as_view()


class ReferalView(TemplateView):
    template_name = "account/dashboard/investment/referal.html"


modified_referal_view = ReferalView.as_view()


class BonusView(TemplateView):
    template_name = "account/dashboard/investment/bonus.html"


modified_bonus_view = BonusView.as_view()


class WhatsappView(TemplateView):
    template_name = "account/dashboard/investment/whatsapp.html"


modified_whatsapp_view = WhatsappView.as_view()


class JobsView(TemplateView):
    template_name = "account/dashboard/investment/jobs.html"


modified_jobs_view = JobsView.as_view()


class InvestplanView(TemplateView):
    template_name = "account/dashboard/investment/investment_plan.html"

modified_investplan_view = InvestplanView.as_view()


class InvestorderView(TemplateView):
    template_name = "account/dashboard/investment/investment_order.html"


modified_investorder_view = InvestorderView.as_view()

class InvestrecordView(TemplateView):
    template_name = "account/dashboard/investment/investment_record.html"


modified_investrecord_view = InvestrecordView.as_view()


class AcademicView(TemplateView):
    template_name = "account/dashboard/investment/academic_writing_accounts.html"


modified_academic_view = AcademicView.as_view()


class LoansView(TemplateView):
    template_name = "account/dashboard/investment/loans.html"


modified_loans_view = LoansView.as_view()


class VipView(TemplateView):
    template_name = "account/dashboard/investment/vip.html"


modified_vip_view = VipView.as_view()
