from django.urls import reverse, path, include


from .views import invest, plans, plan

app_name = "invest"

urlpatterns = [
    path("registration/", invest, name="invest"),
    path("plans/", plans, name="plans"),
    path("<plan_slug>/<plan_id>/", plan, name="plan"),
]
