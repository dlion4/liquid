import contextlib
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import Transaction
from .serializers import TransactionSerializer


# Create your views here.
class TransactionFilterView(LoginRequiredMixin, View):
    transaction = Transaction

    def get_transaction(self):
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
                    self.get_transaction(), many=True
                ).data,
            }
        )
