from django.http import JsonResponse
from django.views.generic import TemplateView

from amiribd.dashboard.views import DashboardViewMixin
from amiribd.invest.models import Account
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import TransferMoneyForm


class WalletViewMixin(DashboardViewMixin):
    queryset = Account


class WalletView(WalletViewMixin, TemplateView):
    template_name = "account/dashboard/v1/investment/wallet/main.html"
    form_class = TransferMoneyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transfer_money_form"] = self.form_class(request=self.request)
        return context


class WalletSendMoneyView(WalletViewMixin, TemplateView):
    template_name = "account/dashboard/v1/investment/wallet/send.html"


class WalletWithdrawMoneyView(WalletViewMixin, TemplateView):
    template_name = "account/dashboard/v1/investment/wallet/withdraw.html"


class WalletDepositMoneyView(WalletViewMixin, TemplateView):
    template_name = "account/dashboard/v1/investment/wallet/deposit.html"


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def upgrade_plan_account(request, *args, **kwargs):
    return JsonResponse({}, status=200)
