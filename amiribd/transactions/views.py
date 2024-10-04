import contextlib
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import View

from amiribd.subscriptions.views import SubscriptionPlanView

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
        """
        Get all the transaction for the current user
        Returns: dict with transaction summary
        context = super().get_context_data(**kwargs)
        context["transactions_summary"] = self.get_account_transactions()
        return context

        Args: dict[str, Any]
        Returns: Args
        """
        context =  super().get_context_data(**kwargs)
        context["transactions_summary"] = self.get_account_transactions()[:6]
        return context



