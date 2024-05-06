from django.http import HttpResponseRedirect
from django.urls import reverse, path

from .views import generate_referral

app_name = "htmx"

urlpatterns = [
    path("<profile_id>/", generate_referral, name="generate_referral_code"),
]
