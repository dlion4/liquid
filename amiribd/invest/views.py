import json
from decimal import Decimal  # Import Decimal from the decimal module
from typing import Any
from django.core.cache import cache 
from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db import transaction
from django.db.models import Sum
from django.http import HttpRequest
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from amiribd.dashboard.views import DashboardGuard
from amiribd.dashboard.views import DashboardViewMixin
from amiribd.jobs.forms import JobApplicationForm
from amiribd.jobs.models import Job
from amiribd.payments.helpers import MpesaStkPushSetUp
from amiribd.profiles.forms import AgentForm
from amiribd.profiles.forms import PlantformForm
from amiribd.profiles.models import PlantformType
from amiribd.schemes.forms import WhatsAppEarningSchemeForm
from amiribd.schemes.models import WhatsAppEarningScheme
from amiribd.shops.forms import ShopItemForm
from amiribd.shops.forms import ShopItemOfferForm
from amiribd.shops.models import ShopItem
from amiribd.transactions.models import Transaction
from amiribd.users.models import Profile
from amiribd.users.views import send_welcome_email

from .forms import AccountEventWithdrawalForm
from .forms import AccountRegistrationForm
from .forms import AddPlanForm
from .forms import CancelPlanForm
from .forms import PlanRegistrationForm
from .forms import PoolRegistrationForm
from .models import Account
from .models import AccountType
from .models import Plan
from .models import PlanType
from .models import Pool
from .models import PoolType
from .models import SavingPlan
from .serializers import AccountSerializer
from .serializers import PlanSerializer
from .serializers import PoolSerializer

# Create your views here.


class InvestmentSetupView(DashboardGuard, TemplateView):
    template_name = ""

    def dispatch(self, request, *args, **kwargs):
        if (
            not Pool.objects.filter(profile=self._get_user().profile_user).exists()
            and request.resolver_match.view_name != "dashboard:invest:invest"
        ):
            return redirect(reverse("dashboard:invest:invest"))
        return super().dispatch(request, *args, **kwargs)


class InvestmentRegistrationView(InvestmentSetupView):
    form_class = PoolRegistrationForm
    template_name = "account/dashboard/v1/investment/setup.html"
    # template_name = "account/dashboard/investment/setup.html"  # noqa: ERA001
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
            AccountType, pk=request.GET.get("account_type_id"),
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
            },
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
            },
        )


class HandlePaymentCreateTransactionView(LoginRequiredMixin, View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        print(request.body)

        profile = request.user.profile_user
        data = json.loads(request.body)
        phone_number = data.get("phone_number")
        currency=data.get("currency", "KES")
        country = data.get("country", "Kenya")
        pool = Pool.objects.get(profile=profile, pk=kwargs.get("pool_id"))
        account = Account.objects.get(
            pool=pool, pool__profile=profile, pk=kwargs.get("account_id"),
        )
        plan = Plan.objects.get(
            account=account, account__pool__profile=profile, pk=kwargs.get("plan_id"),
        )

        total_investment = sum(
            instance.type.price for instance in [pool, account, plan])

        discountPrice = Decimal(Decimal("0.2") * Decimal(total_investment))  # noqa: N806
        # discountPrice = Decimal(total_investment)  # noqa: ERA001

        mpesa_code = data.get("mpesa_transaction_code")
        phone_number = data.get("phone_number")

        transaction = Transaction.objects.create(
            profile=profile,
            account=account,
            type="DEPOSIT",
            amount=total_investment,
            discount=discountPrice,
            source="Account Registration",
            payment_phone=phone_number,
            mpesa_transaction_code=mpesa_code,
            payment_phone_number=phone_number,
            currency=currency,
            country=country,
        )
        # plan.is_paid = True  # noqa: ERA001
        plan.mpesa_transaction_code = mpesa_code
        plan.payment_phone_number = phone_number
        plan.save()

        account.balance = Decimal(Decimal(account.balance) + Decimal(transaction.paid))
        account.save()

        # look for the referrer
        profile = pool.profile

        profile.plans.add(plan)

        profile.save()

        self.__get_referrer_and_update_account(
            profile, mpesa_code, phone_number, currency)

        return JsonResponse(
            {"success": True, "url": reverse_lazy("subscriptions:list")},
        )

    def __get_referrer_and_update_account(
        self, profile, mpesa_code, phone_number, currency="KES", country="Kenya"):
        if referrer := profile.referred_by:
            # update the referrer account

            referrer_profile = referrer.profile_user
            referrer_profile_account = Account.objects.get(
                pool__profile=referrer_profile,
            )
            transaction = Transaction.objects.create(
                profile=Profile.objects.get(referred_by=referrer),
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
        account=account, account__pool__profile=profile, pk=request.GET.get("plan_pk"),
    )
    total_investment = sum(instance.type.price for instance in [pool, account, plan])
    discountPrice = Decimal(Decimal("0.2") * Decimal(total_investment))  # noqa: N806
    amount_to_be_paid = total_investment - discountPrice
    return JsonResponse({"amount": amount_to_be_paid})


class HandlePaymentView(LoginRequiredMixin, View):


    @method_decorator(csrf_exempt, name="dispatch")
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        plan = Plan.objects.filter(
            account__pool__profile__id=request.GET.get("profile")).last()
        plan = PlanSerializer(plan).data
        return JsonResponse({"success": True, "plan": plan})


class HandleRegistrationPaymentView(HandlePaymentView):

    def post(self, request, *args, **kwargs):
        json.loads(request.body)
        #TODO: CREATE THE PLAN SECTION
        
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
        # plan = get_object_or_404(Plan, type=plan_type)  # noqa: ERA001
        plan, _ = Plan.objects.get_or_create(
            account=account,
            type=plan_type,
            payment_method=data.get("payment_method", "PAYBILL"),
            mpesa_transaction_code=transactioncode,
            payment_phone_number=phone_number,
        )
        # check if the the user has the plan already

        # Check if the user already has this plan
        if profile.plans.filter(id=plan.id).exists():
            return JsonResponse(
                {"error": "Plan already exists in the profile", "success": False},
                status=400,
            )
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
        account.balance += Decimal(amount)
        account.save()


        send_welcome_email.after_response(
            profile.user,
            "mails/add_plan.html",
            {
                "user": profile.user,
                "plan": plan,
                "subject": "Earnkraft Agencies [Plan purchase Successful]",
            },
        )

        return JsonResponse(
            {
                "success": True,
                "url": reverse(
                    "subscriptions:subscription",
                    kwargs={"plan_slug":plan.slug,"plan_id":plan.pk}),
            },
        )

    def handle_transaction_creation(  # noqa: PLR0913
            self,
            request,
            profile,
            account,
            amount,
            phone_number,
            transactioncode,
            currency="KES",
            country="Kenya",
        )->None:
         Transaction.objects.create(
            profile=profile,
            account=account,
            type="DEPOSIT",
            amount=amount,
            is_payment_success=True,
            source="Account Registration",
            payment_phone=phone_number,
            mpesa_transaction_code=transactioncode,
            payment_phone_number=phone_number,
            currency=currency,
            country=country,
        )



def check_payment_status(request):
    service = MpesaStkPushSetUp().mpesa_stk_push_service()
    response = service.collect.status(invoice_id=request.GET.get("invoice_id"))
    return JsonResponse({"success": True, "response": response})


class InvestmentSchemeView(InvestmentSetupView, DashboardViewMixin):
    # template_name = "account/dashboard/investment/plans.html"  # noqa: ERA001
    template_name = "account/dashboard/v1/investment/plans.html"
    queryset = Account

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["withdrawal_form"] = AccountEventWithdrawalForm()
        context["add_plan_form"] = AddPlanForm(request=self.request)
        return context


plans = InvestmentSchemeView.as_view()

class InvestmentPlanView(InvestmentSetupView, DashboardViewMixin):
    # template_name = "account/dashboard/investment/plan.html"  # noqa: ERA001
    template_name = "account/dashboard/v1/investment/plan.html"
    htmx_template_name = "account/dashboard/investment/partials/transactions.html"
    queryset = Account
    plan = Plan
    transaction = Transaction

    def __transactions(self):
        return Transaction.objects.filter(
            profile=self._get_user().profile_user,
        ).order_by("-id")

    def get_object(self, **kwargs):
        return get_object_or_404(
            self.plan,
            account__pool__profile=self._get_user().profile_user,
            slug=kwargs.get("plan_slug"),
            pk=kwargs.get("plan_id"),
        )


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
                context["transactions"] = Transaction.objects.filter(
                    type=type_of_transaction, profile=self._get_user().profile_user,
                ).order_by("-id")
            return render(request, self.htmx_template_name, context)
        return super().get(request, *args, **kwargs)


plan = InvestmentPlanView.as_view()

# modified view way of creating views


class InvestmentViewMixin(DashboardViewMixin):
    queryset = Account

    def get_profile(self):
        return get_user(self.request).profile_user


class WithdrawView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/withdrawal.html"  # noqa: ERA001
    template_name = "account/dashboard/v1/investment/withdrawal.html"


modified_withdrawal_view = WithdrawView.as_view()


class WalletView(InvestmentViewMixin):
    template_name = "account/dashboard/v1/investment/wallet.html"


modified_wallet_view = WalletView.as_view()


class ReferralView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/referal.html"  # noqa: ERA001
    template_name = "account/dashboard/v1/investment/referal.html"


modified_referal_view = ReferralView.as_view()


class QinfoView(InvestmentViewMixin):
    template_name = "account/dashboard/v1/investment/qinfo.html"

modified_qinfo_view = QinfoView.as_view()

class ComingSoonView(InvestmentViewMixin):
    template_name = "account/dashboard/v1/investment/comingsoon.html"

modified_comingsoon_view = ComingSoonView.as_view()

class AdvertiseView(InvestmentViewMixin):
    template_name = "account/dashboard/v1/investment/advertise.html"

modified_advertise_view = AdvertiseView.as_view()

class MonetizeView(InvestmentViewMixin):
    template_name = "account/dashboard/v1/investment/monetize.html"

modified_monetize_view = MonetizeView.as_view()




class BonusView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/bonus.html"  # noqa: ERA001
    template_name = "account/dashboard/v1/investment/bonus.html"


modified_bonus_view = BonusView.as_view()



class WhatsappView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/whatsapp.html"  # noqa: ERA001
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
                self.request, "Upload submitted successfully. Wait for approval!",
            )

            return redirect(self.success_url)

        messages.error(self.request, "Upload failed. Please try again!")
        return redirect(self.success_url)


modified_whatsapp_view = WhatsappView.as_view()



class JobsView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/jobs.html"  # noqa: ERA001
    template_name = "account/dashboard/v1/investment/jobs.html"
    jobs =Job
    job_application_form = JobApplicationForm

    def get_jobs(self):
        return self.jobs.objects.all().order_by("-id")

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["jobs"] = self.get_jobs()
        context["job_application_form"] = self.job_application_form(job_id=1, applicant_id=1)  # noqa: E501
        return context

modified_jobs_view = JobsView.as_view()


def obtain_all_job_type(request):
    jobs = Job.objects.all().order_by("-id")
    job_application_form = JobApplicationForm(job_id=1, applicant_id=1) 
    return render(
        request,
        "account/dashboard/v1/investment/jobs/partials.html",
        {
            "jobs": jobs,
            "job_application_form": job_application_form
        }
    )


def fetch_job_type(request, location_type: str):
    if location_type == "*":
        jobs = Job.objects.all().order_by("-id")
    else:
        jobs = Job.objects.filter(location_type__iexact=location_type).order_by("-id")
    job_application_form = JobApplicationForm(job_id=1, applicant_id=1)
    
    return render(
        request,
        "account/dashboard/v1/investment/jobs/partials.html",
        {
            "jobs": jobs,
            "job_application_form": job_application_form
        }
    )
class InvestPlanView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/investment_plan.html"  # noqa: E501, ERA001
    template_name = "account/dashboard/v1/investment/investment_plan.html"

    def retrieve_investment_schemes_options(self, **kwargs):
        return SavingPlan.objects.filter(is_active=True)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["investment_schemes"] = self.retrieve_investment_schemes_options(**kwargs)  # noqa: E501
        return context


modified_investplan_view = InvestPlanView.as_view()


class InvestOrderView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/investment_order.html"  # noqa: E501, ERA001
    template_name = "account/dashboard/v1/investment/investment_order.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not self.get_profile_plans(**kwargs):
            return redirect("dashboard:invest:invest")
        return super().dispatch(request, *args, **kwargs)


modified_investorder_view = InvestOrderView.as_view()


class InvestRecordView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/investment_record.html"  # noqa: E501, ERA001
    template_name = "account/dashboard/v1/investment/investment_record.html"


modified_investrecord_view = InvestRecordView.as_view()




class AcademicView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/academic_writing_accounts.html"  # noqa: E501, ERA001
    template_name = "account/dashboard/v1/investment/academic_writing_accounts.html"
    shop_item_form = ShopItemForm
    shop_item_offer_form = ShopItemOfferForm

    def get_shop_items(self):
        return ShopItem.objects.select_related("profile").filter(is_sold=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shop_item_form"] = self.shop_item_form()
        context["shop_item_offer_form"] = self.shop_item_offer_form()
        context["shop_items"] = self.get_shop_items()
        return context


modified_academic_view = AcademicView.as_view()


class LoansView(InvestmentViewMixin):
    # template_name = "account/dashboard/investment/loans.html"  # noqa: ERA001
    template_name = "account/dashboard/v1/investment/loans.html"

modified_loans_view = LoansView.as_view()


class VipView(DashboardGuard, InvestmentViewMixin):
    # template_name = "account/dashboard/investment/vip.html"  # noqa: ERA001
    template_name = "account/dashboard/v1/investment/vip.html"
    form_class = AgentForm

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["agent_form"] = self.form_class()
        context["platform_form"] = PlantformForm()
        context["platform_type"] = PlantformType.objects.all()
        return context


modified_vip_view = VipView.as_view()
