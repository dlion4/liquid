from django.urls import include
from django.urls import path

from amiribd.invest.lookups.views import validate_profile_plan_purchase_status

from .views import CheckUserSubscriptionStatusView
from .views import HandleAccountSelectionView
from .views import HandleAddPlanPaymentView
from .views import HandlePaymentCreateTransactionView
from .views import HandlePlanSelectionView
from .views import HandlePoolSelectionView
from .views import HandleRegistrationPaymentView
from .views import InvestMentSavingView
from .views import VerifyTransactionPaymentView
from .views import check_payment_status
from .views import delete_transaction_payment_view
from .views import (
    # fetch_amount_tobe_paid_minus_discount,
    fetch_amount_tobe_paid_plus_discount,
)
from .views import invest
from .views import modified_academic_view  # modified_invest_view,
from .views import modified_bonus_view
from .views import modified_comingsoon_view
from .views import modified_investorder_view
from .views import modified_investplan_view
from .views import modified_investrecord_view
from .views import modified_loans_view
from .views import modified_monetize_view
from .views import modified_qinfo_view
from .views import modified_referal_view
from .views import modified_upgrade_view
from .views import modified_vip_view
from .views import modified_wallet_view
from .views import modified_whatsapp_view
from .views import modified_withdrawal_view
from .views import plan
from .views import plans

app_name = "invest"

urlpatterns = [
    path("registration/", invest, name="invest"),
    path(
        "verify-profile-plans-status/",
        validate_profile_plan_purchase_status,
        name="verify_profile_plan_status",
    ),
    path("plans/", plans, name="plans"),
    path("<plan_slug>/<plan_id>/", plan, name="plan"),
    path(
        "handle-payment/",
        HandleRegistrationPaymentView.as_view(),
        name="handle-payment",
    ),
    path(
        "handle-add-plan-payment/",
        # handle-add-plan-payment
        HandleAddPlanPaymentView.as_view(),
        name="handle-add-plan-payment",
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
        "handle-payment-create-transaction/<pool_id>/<account_id>/<plan_id>/",
        HandlePaymentCreateTransactionView.as_view(),
        name="handle-payment-create-transaction",
    ),
    path(
        "handle-payment-create-transaction/<pool_id>/<account_id>/<plan_id>/verify-transaction/<reference_code>",
        VerifyTransactionPaymentView.as_view(),
        name="verify-payment-transaction",
    ),
    path(
        "handle-payment-create-transaction/<pool_id>/<account_id>/<plan_id>/delete-transaction/<reference_code>",
        delete_transaction_payment_view,
        name="delete-payment-transaction",
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
    path(
        "check-payment-state/",
        check_payment_status,
        name="check-payment-state",
    ),
    # modifies viwes kwa dashboard settings
    path(
        "withdraw/",
        modified_withdrawal_view,
        name="widsthdraw",
    ),
    path(
        "wallet/",
        modified_wallet_view,
        name="wallet",
    ),
    path(
        "referrals/",
        modified_referal_view,
        name="referals",
    ),
    path(
        "bonus/",
        modified_bonus_view,
        name="bonus",
    ),
    path(
        "whatsapp/",
        modified_whatsapp_view,
        name="whatsapp",
    ),
    # jobs related urls
    path("jobs/", include("amiribd.invest.jobs.urls", namespace="jobs")),
    path(
        "investment-savings-schemes/",
        modified_investplan_view,
        name="invest_plan",
    ),
    path(
        "invest-order/",
        modified_investorder_view,
        name="invest-order",
    ),
    path(
        "invest-record/",
        modified_investrecord_view,
        name="invest-record",
    ),
    path(
        "academic-writing-accounts/",
        modified_academic_view,
        name="academic_writing_accounts",
    ),
    path(
        "loans/",
        modified_loans_view,
        name="loans",
    ),
    path(
        "vip/",
        modified_vip_view,
        name="vip",  # vip
    ),
    # paystack callback urls
    path("qinfo/", modified_qinfo_view, name="qinfo"),
    path("comingsoon/", modified_comingsoon_view, name="comingsoon"),
    path("upgrade/", modified_upgrade_view, name="upgrade"),
    path("monetize/", modified_monetize_view, name="monetize"),
    # Custom action
    path(
        "profile/check-subscription-status",
        CheckUserSubscriptionStatusView.as_view(),
        name="profile-is-subscribed",
    ),
    path(
        "handle-investment-savings/",
        InvestMentSavingView.as_view(),
        name="investment-savings",
    ),
]
