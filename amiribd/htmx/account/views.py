from typing import Any
from django.shortcuts import get_object_or_404
from django.views.generic import View
from amiribd.invest.forms import AccountEventWithdrawalForm, AddPlanForm, CancelPlanForm
from amiribd.invest.models import Account, Plan, PlanType
from amiribd.invest.serializers import PlanTypeSerializer
from amiribd.transactions.models import Transaction
from amiribd.users.models import Profile
from django.contrib.auth import get_user
from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms import model_to_dict
from amiribd.invest.serializers import PlanSerializer
from django.db import transaction
import after_response


class AvailableAmount(View):

    def __get_user(self):
        return get_user(self.request)

    def get_account(self):
        profile = Profile.objects.get(user=self.__get_user())
        return Account.objects.get(pool__profile=profile)

    def __user_withdrawable_input(self):
        return self.request.GET.get("amount", 0)

    def get(self, request, *args, **kwargs):
        account = self.get_account()
        if account.withdrawable_investment < Decimal(self.__user_withdrawable_input()):
            return HttpResponse(
                f"<span class='errorlist'>Insufficent funds: Available amount is {account.withdrawable_investment}</span>"
            )
        return HttpResponse(
            f"<span class='text-success'>Amount available for withdrawal: {account.withdrawable_investment}</span>"
        )


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
            instance = form.save(commit=False)
            amount = form.cleaned_data["amount"]
            account = self.get_account()
            if account.withdrawable_investment > amount:
                return self._validate_account_balance_and_create_transaction(
                    amount, account, instance, profile
                )
            else:
                return JsonResponse({"success": False, "message": "Insufficent funds"})
        return JsonResponse({"success": False, "message": form.errors}, status=400)

    # TODO Rename this here and in `post`
    def _validate_account_balance_and_create_transaction(
        self, amount, account, instance, profile
    ):
        account.balance -= amount
        account.save()
        instance.account = account
        instance.save()
        # create a transaction record for reference purposes
        Transaction.objects.create(
            profile=profile,
            account=account,
            type="WITHDRAWAL",
            amount=amount,
            discount=0,
            paid=0,
            source="Interest withdrawal",
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
                "<span class='text-success' id='plan-item-found'>Plan found</span>"
            )
        return HttpResponse(
            "<span class='text-danger' id='plan-not-found'>Plan not found</span>"
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
            user = Profile.objects.get(pk=user_id)
            plan.status = "RUNNING"
            plan.save()
            print(plan, user)
            return JsonResponse(
                {"success": True, "plan_id": plan_id, "user_id": user_id}
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})


class FilterPlanTypePriceView(HtmxDispatchView):

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        return {
            "add_plan_form": AddPlanForm(
                self.request.POST or None, request=self.request
            )
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
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
                    form, account, request
                )
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)})
        return JsonResponse({"success": False, "message": form.errors}, status=400)

    # TODO Rename this here and in `post`
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
        account = Account.objects.get(pool__profile=profile)

        plan.save()

        return JsonResponse({"success": True})


class HandlePlanPaymentFailedView(HtmxDispatchView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print(data)
        profile = get_object_or_404(Profile, pk=data.get("profile_id"))
        plan = get_object_or_404(
            Plan, account__pool__profile=profile, pk=data.get("plan_id")
        )
        account = get_object_or_404(Account, pool__profile=profile)

        account.balance -= plan.type.price
        account.save()

        plan.delete()

        self.__delete_transaction(account, profile)

        return JsonResponse({"success": True})

    def __delete_transaction(self, account, profile) -> None:
        transaction = Transaction.objects.filter(
            profile=profile, account=account, source="Plan purchase", type="DEPOSIT"
        ).latest()
        if transaction is not None:
            transaction.delete()
        return None

    def get(self, request, *args, **kwargs):
        return JsonResponse({"success": True, "data": None})


class HandlePlanPaymentSuccessView(HtmxDispatchView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        profile = get_object_or_404(Profile, pk=data.get("profile_id"))
        plan = get_object_or_404(
            Plan, account__pool__profile=profile, pk=data.get("plan_id")
        )
        account = get_object_or_404(Account, pool__profile=profile)
        plan.status = "RUNNING"
        plan.is_paid = True
        account.balance += plan.type.price
        account.save()
        plan.save()
        self.__create_transaction(
            profile, account, plan.type.price, data.get("payment_phone")
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
