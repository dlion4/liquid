from django.urls import path

from . import views

app_name = "wallet"


urlpatterns = [
    path("", views.WalletView.as_view(), name="wallet"),
    path("send/", views.WalletSendMoneyView.as_view(), name="send-to-wallet"),
    path(
        "withdraw/",
        views.WalletWithdrawMoneyView.as_view(),
        name="withdraw-from-wallet",
    ),
    path("deposit/", views.WalletDepositMoneyView.as_view(), name="deposit-to-wallet"),
]
