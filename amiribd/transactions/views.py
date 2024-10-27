import contextlib
import json
from typing import Any

from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.http import JsonResponse
from django.views.generic import View

from amiribd.invest.models import Account
from amiribd.invest.models import Pool
from amiribd.subscriptions.views import SubscriptionPlanView
from amiribd.transactions.forms import AccountDepositModelForm

from .models import Transaction
from .serializers import TransactionSerializer


# Create your views here.
class TransactionFilterView(LoginRequiredMixin, View):
    transaction = Transaction

    def get_transaction(self):
        """
        This function uses context to get the transaction object and then
        Prevent any occurrence of transaction not found error that might break the transaction

        Returns: Transaction object

        return self.transaction.objects.filter(
            profile=self.request.user.profile_user,
        ).select_related("profile")
        """  # noqa: E501
        with contextlib.suppress(Exception):
            return self.transaction.objects.filter(
                profile=self.request.user.profile_user,
            ).select_related("profile")

    def get(self, request, *args, **kwargs):
        type_name = self.request.GET.get("type_of_transaction")
        if transaction := self.get_transaction():
            instance = self.get_transaction().filter(type=type_name)
            transaction = TransactionSerializer(instance, many=True)
            return JsonResponse({"transactions": transaction.data, "success": True})

        return JsonResponse(
            {
                "success": True,
                "transactions": TransactionSerializer(
                    self.get_transaction(), many=True).data,
            },
        )

class SubscriptionTransactionListAccountView(SubscriptionPlanView):
    template_name = "account/dashboard/v1/subscriptions/transactions.html"

    def get_object(self)->None:
        return None

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["transactions_summary"] = self.get_account_transactions()[:6]
        return context



class SubscriptionTopupAccountDepositView(LoginRequiredMixin, View):
    def post(self, request:HttpRequest, *args, **kwargs):
        form = AccountDepositModelForm(request=request, data=json.loads(request.body))
        if form.is_valid():
            profile = get_user(request).profile_user
            pool = Pool.objects.get(profile=profile)
            account = Account.objects.get(pool=pool)
            data = {
                "poolId": pool.pk,
                "accountId": account.pk,
                "planId": profile.plans.latest().pk,
                "amount": form.cleaned_data["amount"],
                "profileUserId": profile.pk,
                "emailAddress": profile.user.email,
            }
            return JsonResponse(data, safe=False)
        return JsonResponse({"message": "This is data test for the account update"})
