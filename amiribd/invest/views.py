import contextlib
from django.contrib import messages
import json
from typing import Any
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import FormView, TemplateView
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from intasend import APIService
from amiribd.jobs.forms import JobApplicationForm
from amiribd.payments.helpers import MpesaStkPushSetUp
from amiribd.profiles.models import PlantformType
from amiribd.shops.models import ShopItem
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
from django.contrib.auth import get_user
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import AccountType, PlanType, Pool, Account, Plan, PoolType
from amiribd.dashboard.views import DashboardGuard, DashboardViewMixin
from decimal import Decimal  # Import Decimal from the decimal module
from django.utils.termcolors import colorize
from amiribd.transactions.models import Transaction
from .serializers import AccountSerializer, PlanSerializer, PoolSerializer

from amiribd.profiles.forms import (
    AgentForm,
    PlantformForm,
    PlantformTypeForm,
    PositionForm,
)

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
    template_name = "account/dashboard/v1/investment/setup.html"
    # template_name = "account/dashboard/investment/setup.html"
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
        currency=data.get("currency", "KES")
        country = data.get("country", "Kenya")
        pool = Pool.objects.get(profile=profile, pk=kwargs.get("pool_id"))
        account = Account.objects.get(
            pool=pool, pool__profile=profile, pk=kwargs.get("account_id")
        )
        plan = Plan.objects.get(
            account=account, account__pool__profile=profile, pk=kwargs.get("plan_id")
        )

        totalInvestment = sum(instance.type.price for instance in [pool, account, plan])

        discountPrice = Decimal(Decimal("0.2") * Decimal(totalInvestment))
        # discountPrice = Decimal(totalInvestment)

        mpesa_code = data.get("mpesa_transaction_code")
        phone_number = data.get("phone_number")

        transaction = Transaction.objects.create(
            profile=profile,
            account=account,
            type="DEPOSIT",
            amount=totalInvestment,
            discount=discountPrice,
            source="Account Registration",
            payment_phone=phone_number,
            mpesa_transaction_code=mpesa_code,
            payment_phone_number=phone_number,
            currency=currency,
            country=country,
        )
        # plan.is_paid = True
        plan.mpesa_transaction_code = mpesa_code
        plan.payment_phone_number = phone_number
        plan.save()

        account.balance = Decimal(Decimal(account.balance) + Decimal(transaction.paid))
        account.save()

        # look for the referrer
        profile = pool.profile

        profile.plans.add(plan)

        profile.save()

        self.__get_referrer_and_update_account(profile, mpesa_code, phone_number, currency)

        return JsonResponse(
            {"success": True, "url": reverse_lazy("subscriptions:list")}
        )

    def __get_referrer_and_update_account(self, profile, mpesa_code, phone_number, currency="KES", country="Kenya"):
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
                mpesa_transaction_code=mpesa_code,
                payment_phone_number=phone_number,
                currency=currency,
                country=country,
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


class HandlePaymentView(LoginRequiredMixin, View):


    @method_decorator(csrf_exempt, name="dispatch")
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print(request.GET)
        plan = Plan.objects.filter(account__pool__profile__id=request.GET.get('profile')).last()
        plan = PlanSerializer(plan).data
        return JsonResponse({"success": True, 'plan': plan})


class HandleRegistrationPaymentView(HandlePaymentView):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print(data)
        return JsonResponse({"success": True})
    
class HandleAddPlanPaymentView(HandlePaymentView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        profile = get_object_or_404(Profile, pk=data.get("profile"))
        account = get_object_or_404(Account, pool__profile=profile)
        plan_type = get_object_or_404(PlanType, pk=data.get("plan"))
        amount = data.get("actualAmount", "pay_amount")
        transactioncode = data.get("transactioncode")
        phone_number = data.get("phone_no")
        # plan = get_object_or_404(Plan, type=plan_type)
        plan, _ = Plan.objects.get_or_create(
            account=account,
            type=plan_type,
            payment_method=data.get("payment_method", "PAYBILL"),
            mpesa_transaction_code=transactioncode,
            payment_phone_number=phone_number
        )
        # check if the the user has the plan already
        is_in_profile = profile.plans

        # Check if the user already has this plan
        if profile.plans.filter(id=plan.id).exists():
            return JsonResponse({'error': 'Plan already exists in the profile', 'success': False}, status=400)
        
        # Add the plan to the profile if it does not exist
        profile.plans.add(plan)

        self.handle_transaction_creation(
            request,
            profile=profile,
            account=account,
            amount=amount,
            phone_number=phone_number,
            transactioncode=transactioncode,
            currency=data.get("currency", "KES"),
            country=data.get("country", "Kenya"),
        )

        profile.save()

        return JsonResponse({"success": True, 'url': reverse("subscriptions:subscription", kwargs={
            "plan_slug":plan.slug,
            "plan_id":plan.pk
        })})
    
    def handle_transaction_creation(
            self, 
            request,
            profile,
            account,
            amount,
            phone_number,
            transactioncode,
            currency="KES",
            country="Kenya"
        )->None:
         Transaction.objects.create(
            profile=profile,
            account=account,
            type="DEPOSIT",
            amount=amount,
            is_payment_success=True,
            source='Account Registration',
            payment_phone=phone_number,
            mpesa_transaction_code=transactioncode,
            payment_phone_number=phone_number,
            currency=currency,
            country=country,
        )



def check_payment_status(request):
    service = MpesaStkPushSetUp().mpesa_stk_push_service()
    response = service.collect.status(invoice_id=request.GET.get("invoice_id"))
    print(response)
    return JsonResponse({"success": True, "response": response})


class InvestmentSchemeView(InvestmentSetupView, DashboardViewMixin):
    # template_name = "account/dashboard/investment/plans.html"
    template_name = "account/dashboard/v1/investment/plans.html"
    queryset = Account

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["withdrawal_form"] = AccountEventWithdrawalForm()
        context["add_plan_form"] = AddPlanForm(request=self.request)
        return context


plans = InvestmentSchemeView.as_view()


class InvestmentPlanView(InvestmentSetupView, DashboardViewMixin):
    # template_name = "account/dashboard/investment/plan.html"
    template_name = "account/dashboard/v1/investment/plan.html"
    htmx_template_name = "account/dashboard/investment/partials/transactions.html"
    queryset = Account
    plan = Plan
    transaction = Transaction

    def __transactions(self):
        return Transaction.objects.filter(
            profile=self._get_user().profile_user
        ).order_by("-id")

    def get_object(self, **kwargs):
        plan = get_object_or_404(
            self.plan,
            account__pool__profile=self._get_user().profile_user,
            slug=kwargs.get("plan_slug"),
            pk=kwargs.get("plan_id"),
        )

        return plan

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["plan"] = self.get_object(**kwargs)
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


class InvestmentViewMixin(DashboardViewMixin):
    queryset = Account

    def get_profile(self):
        return get_user(self.request).profile_user


class WidsthdrawView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/withdrawal.html"
    template_name = "account/dashboard/v1/investment/withdrawal.html"


modified_widthdrawal_view = WidsthdrawView.as_view()


class WalletView(InvestmentViewMixin):
    template_name = "account/dashboard/v1/investment/wallet.html"


modified_wallet_view = WalletView.as_view()


class ReferalView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/referal.html"
    template_name = "account/dashboard/v1/investment/referal.html"


modified_referal_view = ReferalView.as_view()


class BonusView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/bonus.html"
    template_name = "account/dashboard/v1/investment/bonus.html"


modified_bonus_view = BonusView.as_view()

from amiribd.schemes.forms import WhatsAppEarningSchemeForm
from amiribd.schemes.models import WhatsAppEarningScheme
from django.db import models
from django.db.models import Sum


class WhatsappView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/whatsapp.html"
    template_name = "account/dashboard/v1/investment/whatsapp.html"

    form_class = WhatsAppEarningSchemeForm

    success_url = "dashboard:invest:whatsapp"

    def get_total_whatsapp_earnings(self):
        earnings = (
            WhatsAppEarningScheme.objects.prefetch_related("profile")
            .filter(profile=self.get_profile(), approved=True)
            .aggregate(total=Sum(models.F("views") * models.F("price")))
        )

        if earnings["total"]:
            return Decimal(earnings["total"])
        return Decimal("0.00")

    def get_whatsapp_earning_schemes(self):
        return (
            WhatsAppEarningScheme.objects.prefetch_related("profile")
            .filter(
                profile=self.get_profile(),
            )
            .order_by("-id")
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.get_total_whatsapp_earnings()
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        context["earnings"] = self.get_total_whatsapp_earnings()
        context["whatsappschemestate"] = self.get_whatsapp_earning_schemes()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.profile = self.get_profile()
            instance.save()
            form.save()

            messages.success(
                self.request, "Upload submitted successfully. Wait for approval!"
            )

            return redirect(self.success_url)

        else:
            messages.error(self.request, "Upload failed. Please try again!")
            return redirect(self.success_url)


modified_whatsapp_view = WhatsappView.as_view()

from amiribd.jobs.models import Job

class JobsView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/jobs.html"
    template_name = "account/dashboard/v1/investment/jobs.html"
    jobs =Job
    job_application_form = JobApplicationForm

    def get_jobs(self):
        return self.jobs.objects.select_related("author").filter(is_active=True).order_by("?")

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['jobs'] = self.get_jobs()
        context["job_application_form"] = self.job_application_form(job_id=1, applicant_id=1)
        return context
    
 

    


modified_jobs_view = JobsView.as_view()


class InvestplanView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/investment_plan.html"
    template_name = "account/dashboard/v1/investment/investment_plan.html"


modified_investplan_view = InvestplanView.as_view()


class InvestorderView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/investment_order.html"
    template_name = "account/dashboard/v1/investment/investment_order.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not self.get_profile_plans(**kwargs):

            return redirect("dashboard:invest:invest")
            

        return super().dispatch(request, *args, **kwargs)


modified_investorder_view = InvestorderView.as_view()


class InvestrecordView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/investment_record.html"
    template_name = "account/dashboard/v1/investment/investment_record.html"


modified_investrecord_view = InvestrecordView.as_view()


from amiribd.shops.forms import ShopItemForm, ShopItemOfferForm

class AcademicView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/academic_writing_accounts.html"
    template_name = "account/dashboard/v1/investment/academic_writing_accounts.html"
    shop_item_form = ShopItemForm
    shop_item_offer_form = ShopItemOfferForm

    def get_shop_items(self):
        return ShopItem.objects.select_related("profile").filter(is_sold=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_item_form'] = self.shop_item_form()
        context['shop_item_offer_form'] = self.shop_item_offer_form()
        context['shop_items'] = self.get_shop_items()
        return context
    


modified_academic_view = AcademicView.as_view()


class LoansView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/loans.html"
    template_name = "account/dashboard/v1/investment/loans.html"


modified_loans_view = LoansView.as_view()


class VipView(DashboardGuard, InvestmentViewMixin):
    # template_name = "account/dashboard/investment/vip.html"
    template_name = "account/dashboard/v1/investment/vip.html"
    form_class = AgentForm

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["agent_form"] = self.form_class()
        context["platform_form"] = PlantformForm()
        context["platform_type"] = PlantformType.objects.all()
        return context


modified_vip_view = VipView.as_view()
