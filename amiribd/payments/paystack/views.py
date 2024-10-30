import json
from typing import Any
from urllib.parse import unquote
from decimal import Decimal
import requests
from django.contrib.auth import get_user
from django.http import HttpRequest
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.core.exceptions import ValidationError

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

        return JsonResponse(
            {
                "reference": "reference",
                "status": "paystack_reference_data.get('status')",
            }
        )


class PayStackPaymentStatusView(View):
    invest_saving_form = InvestMentSavingForm  # Assume this is your form class

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def _get_profile(self):
        """Helper method to retrieve the user's profile."""
        return get_user(self.request).profile_user

    def get(self, request, *args, **kwargs):

        return JsonResponse({"message": "Hello there"}, status=200)
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print(data)
        # try:
        return JsonResponse({
            "update_transaction_url": reverse(
                "payments:paystack:paystack_saving_investment_payment_complete_create_transaction"
            ),
            "reason": data.get("reason", ""),
            "success": True,
        }, status=200)
        # except (ValueError, ValidationError) as e:
        #     return JsonResponse({"error": str(e)}, status=400)


class TransactionSavingsInvestmentPaymentView(CustomTransactionCreationView):
    def _get_profile(self):
        return get_user(self.request).profile_user

    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        account: Account = Account.objects.filter(
            pool__profile=self._get_profile(),
        ).latest()
        transaction = self.create_transaction_method(
            profile=self._get_profile(),
            account=account,
            amount=data.get("amount"),
            source="Savings & Investment",
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
