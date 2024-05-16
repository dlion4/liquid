from django.urls import reverse, path, include

from . import views


app_name = "account"

urlpatterns = [
    path("available_amount/", views.AvailableAmount.as_view(), name="available_amount"),
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
]
