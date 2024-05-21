from amiribd.dashboard.views import DashboardViewMixin
from amiribd.invest.models import Account
from django.views.generic import TemplateView


class WalletViewMixin(DashboardViewMixin):
    queryset = Account


class WalletView(TemplateView):
    template_name = "account/dashboard/v1/investment/wallet/main.html"


class WalletSendMoneyView(TemplateView):
    template_name = "account/dashboard/v1/investment/wallet/send.html"


class WalletWithdrawMoneyView(TemplateView):
    template_name = "account/dashboard/v1/investment/wallet/withdraw.html"


class WalletDepositMoneyView(TemplateView):
    template_name = "account/dashboard/v1/investment/wallet/deposit.html"
