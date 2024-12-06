from django.urls import path

from . import views

app_name = "subscriptions"

urlpatterns = [
    path("", views.SubscriptionAccountView.as_view(), name="home"),
    path("plans/", views.SubscriptionListView.as_view(), name="list"),
    path(
        "subscription-plan/<plan_slug>/<plan_id>/",
        views.SubscriptionPlanView.as_view(),
        name="subscription",
    ),
    # path("update/", views.SubscriptionAccountUpdateView.as_view(), name="update"),
    # path("delete/", views.SubscriptionAccountDeleteView.as_view(), name="delete"),
    # path("list/", views.SubscriptionAccountListView.as_view(), name="list"),
    path("pricing/", views.PlanPricingView.as_view(), name="plans"),
]
