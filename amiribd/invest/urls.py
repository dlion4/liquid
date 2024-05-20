from django.urls import reverse, path, include


from .views import (
    HandleAccountSelectionView,
    HandlePaymentCreateTransactionView,
    HandlePlanSelectionView,
    HandlePoolSelectionView,
    HandleRegistrationPaymentView,
    check_payment_status,
    # fetch_amount_tobe_paid_minus_discount,
    fetch_amount_tobe_paid_plus_discount,
    invest,
    plans,
    plan,
    # mopdified urls here new
    modified_widthdrawal_view,
    modified_wallet_view,
    modified_referal_view,
    modified_bonus_view,
    modified_whatsapp_view,
    modified_jobs_view ,
    # modified_invest_view,
    modified_academic_view,
    modified_loans_view,
    modified_vip_view,
    modified_investplan_view,
    modified_investorder_view, 
    modified_investrecord_view, 



    modified_jobs_view,
    
    modified_loans_view,
    modified_vip_view,
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
        "handle-payment-create-transaction/<pool_id>/<account_id>/<plan_id>/",
        HandlePaymentCreateTransactionView.as_view(),
        name="handle-payment-create-transaction",
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
        "widsthdraw/",
        modified_widthdrawal_view,
        name="widsthdraw",
    ),
    path(
        "wallet/",
        modified_wallet_view,
        name="wallet",
    ),
    path(
        "referals/",
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
    path(
        "jobs/",
        modified_jobs_view,
        name="jobs",
    ),
    path(
        "investment_plan/",
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
        "academic_writing_accounts/",
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
]
