from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("available_amount/", views.AvailableAmount.as_view(), name="available_amount"),
    path(
        "balance/<profile_id>",
        views.AvailableAmountForTransferView.as_view(),
        name="available_amount_for_transfer",
    ),
    path(
        "balance/input/<profile_id>",
        views.input_check_money_to_transfer,
        name="input_amount_for_transfer",
    ),
    path("withdrawal/", views.AccountEventWithdrawalView.as_view(), name="withdrawal"),
    path("cancel-plan/", views.CancelPlanView.as_view(), name="cancel_plan"),
    path(
        "reactivate-plan/<int:plan_id>/<int:user_id>/",
        views.ReactivatePlanView.as_view(),
        name="reactivate_plan",
    ),
    path(
        "plan-type/",
        views.FilterPlanTypePriceView.as_view(),
        name="plan-type",
    ),
    path(
        "plan-payment/handle-payment-failed/",
        views.HandlePlanPaymentFailedView.as_view(),
        name="handle-payment-failed",
    ),
    path(
        "handle-payment-success/",
        views.HandlePlanPaymentSuccessView.as_view(),
        name="handle-payment-success",
    ),
    path(
        "handle-close-payment-form-view/",
        views.HandleClosePaymentFormView.as_view(),
        name="handle-close-payment-form-view",
    ),
]
