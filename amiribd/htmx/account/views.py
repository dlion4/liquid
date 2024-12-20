import json
from decimal import Decimal
from typing import Any

import after_response
from django.contrib import messages
from django.contrib.auth import get_user
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from amiribd.invest.forms import AccountEventWithdrawalForm
from amiribd.invest.forms import AddPlanForm
from amiribd.invest.forms import CancelPlanForm
from amiribd.invest.models import Account
from amiribd.invest.models import Plan
from amiribd.invest.models import PlanType
from amiribd.invest.models import Pool
from amiribd.invest.serializers import PlanSerializer
from amiribd.invest.wallet.forms import TransferMoneyForm
from amiribd.transactions.models import Transaction
from amiribd.users.models import Profile

ALLOWABLE_WITHDRAWAL_AMOUNT = 50


class AvailableAmountViewMixin(View):
    profile = Profile

    def __get_user(self):
        return get_user(self.request)

    def get_profile(self, *args, **kwargs):
        return get_object_or_404(self.profile, pk=kwargs.get("profile_id"))

    def get_account(self):
        profile = Profile.objects.get(user=self.__get_user())
        return Account.objects.get(pool__profile=profile)


class AvailableAmount(AvailableAmountViewMixin):
    def __user_withdrawable_input(self):
        return self.get_amount(self.request)

    def get_amount(self, request):
        switch = {
            "amount": request.GET.get("amount", 0),
            "amount_to_transfer": request.GET.get("amount_to_transfer", 0),
        }

        return switch["amount"] or switch["amount_to_transfer"]

    def get(self, request, *args, **kwargs):
        account = self.get_account()
        amount_to_withdraw = round(
            (Decimal(self.__user_withdrawable_input()) * Decimal("0.85")), 2,
        )
        if Decimal(account.withdrawable_investment) < Decimal(amount_to_withdraw):
            return HttpResponse(
                f"""
                <span class='errorlist'>
                Insufficient funds! Account balance: {account.withdrawable_investment}
                </span>""",
            )
        return HttpResponse(
            f"""<span class='text-success'>
            Amount available for withdrawal: {account.withdrawable_investment}
            before taxes,
            Amount you'll receive after tax: {amount_to_withdraw}
            </span>""",
        )


class AvailableAmountForTransferView(AvailableAmountViewMixin):

    form_class = TransferMoneyForm

    def get_account(self, *args, **kwargs):
        account = Account.objects.filter(
            pool__profile=self.get_profile(*args, **kwargs),
        )
        return account.first() if account.exists() else None

    def get(self, request, *args, **kwargs):
        if account := self.get_account(*args, **kwargs):
            context = (
                {"success": True}
                if account.withdrawable_investment > ALLOWABLE_WITHDRAWAL_AMOUNT
                else {"success": False}
            )
        else:
            context = {}
        return JsonResponse(context)

    def post(self, request, *args, **kwargs):
        profile = self.get_profile(*args, **kwargs)
        destination_account = int(request.POST.get("destination_account"))
        amount_to_be_transferred = Decimal(request.POST.get("amount_to_transfer"))
        # get the transferer account
        sender_account = self.get_account(*args, **kwargs)
        receiver_account = get_object_or_404(Account, pk=destination_account)
        # debit the sender account and then credit the receiver account
        sender_account.balance -= amount_to_be_transferred
        sender_account.save()
        # create a withdrawal transaction
        Transaction.objects.create(
            profile=profile,
            account=sender_account,
            type="WITHDRAWAL",
            amount=amount_to_be_transferred,
            discount=0,
            source=f"Transfer to {receiver_account.pool.profile} Account",
        )

        receiver_account.balance += amount_to_be_transferred
        receiver_account.save()

        Transaction.objects.create(
            profile=profile,
            account=receiver_account,
            type="DEPOSIT",
            amount=amount_to_be_transferred,
            discount=0,
            source=f"Transfer from {profile} Account",
        )

        messages.success(
            request,
            f"""
            You've successfully transferred
            {amount_to_be_transferred} to {destination_account}""",
        )
        return redirect("users:profile:wallet:wallet")


def input_check_money_to_transfer(request, profile_id):
    amount = Decimal(request.GET.get("amount_to_transfer"))
    account = get_object_or_404(
        Account, pool__profile__pk=profile_id, pool__profile=request.user.profile_user,
    )
    if Decimal(account.withdrawable_investment) > amount:
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


# class HandleAmountTransferView()
class AccountEventWithdrawalView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_profile(self):
        return Profile.objects.get(user=get_user(self.request))

    def get_account(self):
        profile = self.get_profile()
        return Account.objects.get(pool__profile=profile)

    def post(self, request, *args, **kwargs):
        form = AccountEventWithdrawalForm(request.POST)
        profile = self.get_profile()
        if form.is_valid():
            return self._handle_withdrawal_logic_here(form, profile)
        return JsonResponse({"success": False, "message": form.errors}, status=400)

    def _handle_withdrawal_logic_here(self, form, profile):
        instance = form.save(commit=False)
        amount = Decimal(form.cleaned_data.get("amount", 0))
        account = self.get_account()
        if account.withdrawable_investment > Decimal(amount):
            return self._validate_account_balance_and_create_transaction(
                amount, account, instance, profile)
        return JsonResponse({"success": False, "message": "Insufficient funds"})

    def _validate_account_balance_and_create_transaction(
        self, amount, account:Account, instance, profile):
        account.balance -= amount
        account.save()
        instance.account = account
        instance.save()
        amount_paid = amount * Decimal("0.85")
        Transaction.objects.create(
            profile=profile,
            account=account,
            type="WITHDRAWAL",
            amount=amount_paid,
            discount=0,
            paid=0,
            source="Profits withdrawal",
        ).save()
        return JsonResponse({"success": True})


class HtmxDispatchView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CancelPlanView(HtmxDispatchView):

    def __get_user_plan(self):
        user_input = self.request.GET.get("plan")
        return Plan.objects.filter(type__type=user_input).first()

    def get(self, request, *args, **kwargs):
        plan = self.__get_user_plan()
        if plan is not None:
            return HttpResponse(
                """
                <span class='text-success' id='plan-item-found'>
                Plan found</span>""",
            )
        return HttpResponse(
            """
            <span class='text-danger' id='plan-not-found'>
            Plan not found</span>""",
        )

    def post(self, request, *args, **kwargs):
        form = CancelPlanForm(request.POST)
        if form.is_valid():
            plan = Plan.objects.filter(type__type=form.cleaned_data["plan"]).first()
            if plan is not None:
                plan.status = "CANCELLED"
                plan.save()
                return JsonResponse({"success": True})
            return JsonResponse({"success": False, "message": "Plan not found"})
        return JsonResponse({"success": False, "message": "Invalid input"})


class ReactivatePlanView(HtmxDispatchView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            plan_id = kwargs.get("plan_id")
            user_id = kwargs.get("user_id")
            # Now you can use plan_id and user_id as needed
            plan = Plan.objects.get(pk=plan_id)
            # user = Profile.objects.get(pk=user_id)  # noqa: ERA001
            plan.status = "RUNNING"
            plan.save()
            return JsonResponse(
                {"success": True, "plan_id": plan_id, "user_id": user_id},
            )
        except Exception as e:  # noqa: BLE001
            return JsonResponse({"success": False, "message": str(e)})


class FilterPlanTypePriceView(HtmxDispatchView):

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        return {
            "add_plan_form": AddPlanForm(
                self.request.POST or None,
                request=self.request,
            ),
        }

    def get(self, request, *args, **kwargs):
        # context = self.get_context_data(**kwargs)  # noqa: ERA001
        plan_type_pk = request.GET.get("plan-type")
        plan = PlanType.objects.get(pk=plan_type_pk)
        return JsonResponse({"price": plan.price})

    def get_profile(self):
        return get_user(self.request).profile_user

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = AddPlanForm(request.POST, request=self.request)
        account = Account.objects.get(pool__profile=self.get_profile())
        if form.is_valid():
            try:
                return self._extracted_post_instance_save_and_transaction(
                    form,
                    account,
                    request,
                )
            except Exception as e:  # noqa: BLE001
                return JsonResponse({"success": False, "message": str(e)})
        return JsonResponse({"success": False, "message": form.errors}, status=400)

    @after_response.enable
    def _extracted_post_instance_save_and_transaction(self, form, account, request):
        instance = form.save(commit=False)
        instance.account = account
        instance.account.balance += Decimal(form.cleaned_data["price"])
        instance.account.save()
        instance.save()
        # create a transaction
        Transaction.objects.create(
            profile=request.user.profile_user,
            account=account,
            type="DEPOSIT",
            amount=Decimal(form.cleaned_data["price"]),
            discount=0,
            source="Plan purchase",
        )
        return JsonResponse({"success": True, "plan": PlanSerializer(instance).data})


class PlanPaymentView(HtmxDispatchView):

    def post(self, request, *args, **kwargs):
        plan_id = kwargs.get("plan_id")
        plan = Plan.objects.get(pk=plan_id)

        profile = Profile.objects.get(pk=kwargs.get("profile_id"))
        account = Account.objects.get(pool__profile=profile)  # noqa: F841
        plan.save()
        return JsonResponse({"success": True})


class HandlePlanPaymentFailedView(HtmxDispatchView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        profile = get_object_or_404(Profile, pk=data.get("profile_id"))
        plan = get_object_or_404(
            Plan,
            account__pool__profile=profile,
            pk=data.get("plan_id"),
        )
        account = get_object_or_404(Account, pool__profile=profile)
        account.balance -= plan.type.price
        account.save()
        plan.delete()
        self.__delete_transaction(account, profile)
        return JsonResponse({"success": True})

    def __delete_transaction(self, account, profile) -> None:
        transaction = Transaction.objects.filter(
            profile=profile,
            account=account,
            source="Plan purchase",
            type="DEPOSIT",
        ).latest()
        if transaction is not None:
            transaction.delete()

    def get(self, request, *args, **kwargs):
        return JsonResponse({"success": True, "data": None})


class HandlePlanPaymentSuccessView(HtmxDispatchView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        profile = get_object_or_404(Profile, pk=data.get("profile_id"))
        plan = get_object_or_404(
            Plan,
            account__pool__profile=profile,
            pk=data.get("plan_id"),
        )
        account = get_object_or_404(Account, pool__profile=profile)
        plan.status = "RUNNING"
        plan.is_paid = True
        account.balance += plan.type.price
        account.save()
        plan.save()
        self.__create_transaction(
            profile,
            account,
            plan.type.price,
            data.get("payment_phone"),
        )
        return JsonResponse({"success": True, "url": plan.get_absolute_url()})

    def __create_transaction(self, profile, account, amount, payment_phone):
        Transaction.objects.create(
            profile=profile,
            account=account,
            type="DEPOSIT",
            amount=amount,
            discount=0,
            source="Plan purchase",
            payment_phone=payment_phone,
        )


class HandleClosePaymentFormView(HtmxDispatchView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        profile = get_object_or_404(Profile, pk=data.get("profile_id"))
        pool = get_object_or_404(Pool, profile=profile, pk=data.get("pool_id"))
        pool.delete()
        return JsonResponse({"success": True})
