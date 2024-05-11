from django.urls import reverse, path, include


from .views import (
    HandleAccountSelectionView,
    HandlePaymentPopupView,
    HandlePlanSelectionView,
    HandlePoolSelectionView,
    HandleRegistrationPaymentView,
    check_payment_status,
    # fetch_amount_tobe_paid_minus_discount,
    fetch_amount_tobe_paid_plus_discount,
    invest,
    plans,
    plan,
)

app_name = "invest"

urlpatterns = [
    path("registration/", invest, name="invest"),
    path("plans/", plans, name="plans"),
    path("<plan_slug>/<plan_id>/", plan, name="plan"),
    path(
        "handle-payment/",
        HandleRegistrationPaymentView.as_view(),
        name="handle-payment",
    ),
    path(
        "handle-pool-selection/",
        HandlePoolSelectionView.as_view(),
        name="handle-pool-selection",
    ),
    path(
        "handle-account-selection/",
        HandleAccountSelectionView.as_view(),
        name="handle-account-selection",
    ),
    path(
        "handle-plan-selection/",
        HandlePlanSelectionView.as_view(),
        name="handle-plan-selection",
    ),
    path(
        "handle-payment-popup/",
        HandlePaymentPopupView.as_view(),
        name="handle-payment-popup",
    ),
    path(
        "fetch-amount-to-be-paid-plus-discount/",
        fetch_amount_tobe_paid_plus_discount,
        name="fetch-amount-to-be-paid-plus-discount",
    ),
    path(
        "check-payment-status/",
        check_payment_status,
        name="check-payment-status",
    ),
]
