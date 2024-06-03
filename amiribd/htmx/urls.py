from django.http import HttpResponseRedirect
from django.urls import reverse, path, include

from .views import generate_referral

app_name = "htmx"

urlpatterns = [
    path("<profile_id>/", generate_referral, name="generate_referral_code"),
    path("account/", include("amiribd.htmx.account.urls", namespace="account")),
]
