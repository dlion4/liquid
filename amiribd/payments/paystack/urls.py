from django.urls import path
from . import views

app_name = "paystack"

urlpatterns = [
    path("status/", views.PayStackPaymentCallbackView.as_view(), name="paystack-webhook-callback"),
    path("payment-status/", views.PayStackPaymentStatusView.as_view(), name="paystack-webhook-status")
]

