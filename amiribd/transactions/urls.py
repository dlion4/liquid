from django.urls import path

from . import views

app_name = "transactions"

urlpatterns = [
    path("filter/", views.TransactionFilterView.as_view(), name="filter-transaction"),
    path(
        "transactions/",
        views.SubscriptionTransactionListAccountView.as_view(),
        name="transactions"),
    path(
        "transactions/deposit-account",
        views.SubscriptionTopupAccountDepositView.as_view(),
        name="deposit-account"),
]
