from django.urls import reverse, path, include


from .views import invest, plans

app_name = "invest"

urlpatterns = [
    path("registration/", invest, name="invest"),
    path("plans/", plans, name="plans"),
    ]
