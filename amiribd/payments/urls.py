from django.urls import path, include
from . import views

app_name = "payments"

urlpatterns = [
    path("paystack/", include("amiribd.payments.paystack.urls", namespace="paystack")),
]