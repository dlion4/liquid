import json
from typing import Any

from django.urls import reverse
import requests
from django.contrib.auth import get_user
from django.http import HttpRequest
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from amiribd.invest.forms import InvestMentSavingForm
from amiribd.invest.mixins import CustomTransactionCreationView
from amiribd.invest.models import Account
from amiribd.payments.models import PaystackPaymentStatus
from amiribd.payments.serializers import PaystackPaymentStatusSerializer


class PayStackPaymentCallbackView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        # data = json.loads(request.body)
        # paystack_reference_data = data.get('data')
        # reference = paystack_reference_data.get('reference')
        # status
        """
        1: success
        2: failed
        3: pending
        4: timeout
        """
        # payment_status = PaystackPaymentStatus.objects.create(
        #     email=paystack_reference_data.get('customer').get('email'),
        #     status=paystack_reference_data.get('status'),
        #     reference=reference,
        #     amount=paystack_reference_data.get('amount')/100
        # )

        return JsonResponse({
            "reference": "reference",
            "status":"paystack_reference_data.get('status')",
        })


class PayStackPaymentStatusView(View):
    invest_saving_form = InvestMentSavingForm
    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def _get_profile(self):
        return get_user(self.request).profile_user

    def get(self, request, *args, **kwargs):
        data_context = {}
        if request.GET.get("principal_amount"):
            principal_amount = request.GET.get("principal_amount")
            duration_of_saving_investment = request.GET.get(
                "duration_of_saving_investment")
            interest_amount = request.GET.get("interest_amount")
            expected_daily_interest_plus_amount = request.GET.get(
                "expected_daily_interest_plus_amount",
            )
            instruction = request.GET.get("instruction")
            data_context["principal_amount"] = principal_amount
            data_context["duration_of_saving_investment"] = (
                duration_of_saving_investment)
            data_context["interest_amount"] = interest_amount
            data_context["expected_daily_interest_plus_amount"] = (
                expected_daily_interest_plus_amount)
            data_context["instruction"] = instruction
            form = self.invest_saving_form(data=data_context)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.profile = self._get_profile()
                instance.save()
                form.save()
                return JsonResponse(
                    {
                        "update_transaction_url": reverse(
                            "payments:paystack:paystack_saving_investment_payment_complete_create_transaction",
                        ),
                        "reason": "save_invest",
                        "success": True,
                    },
                    status=200,
                )
        return JsonResponse({"data":"data", "success": True}, safe=False)

class TransactionSavingsInvestmentPaymentView(CustomTransactionCreationView):
    def _get_profile(self):
        return get_user(self.request).profile_user
    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    def post(self,  request, *args, **kwargs):
        data = json.loads(request.body)
        account: Account = Account.objects.filter(
            pool__profile=self._get_profile(),
        ).latest()
        transaction = self.create_transaction_method(
            profile=self._get_profile(),
            account=account,
            amount=data.get("amount"),
            source = "Savings & Investment",
            payment_phone=self._get_profile().user.email,
            mpesa_transaction_code=data.get("reference"),
            payment_phone_number=self._get_profile().user.email,
        )
        transaction.verified = True
        transaction.is_payment_success = True
        transaction.save()
        account.balance += transaction.paid
        account.save()
        return JsonResponse(
            {"success": True, "url": reverse("dashboard:invest:invest-record")},
            status=200,
        )
