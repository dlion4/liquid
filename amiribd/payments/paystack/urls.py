from django.urls import path
from . import views

app_name = "paystack"

urlpatterns = [
    path(
        "status/",
        views.PayStackPaymentCallbackView.as_view(),
        name="paystack-webhook-callback",
    ),
    path(
        "payment-status/",
        views.PayStackPaymentStatusView.as_view(),
        name="paystack-webhook-status",
    ),
    path(
        "payment-success/paystack-saving-investment-payment-complete-create-transaction",
        views.TransactionSavingsInvestmentPaymentView.as_view(),
        name="paystack_saving_investment_payment_complete_create_transaction",
    ),
]
