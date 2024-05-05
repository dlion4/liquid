from django.urls import path
from . import views

app_name = "kyc"

urlpatterns = [
    path("kyc/detail/", views.kyc_profile_detail, name="detail"),
    path("kyc/address/", views.kyc_profile_address, name="address"),
    path("kyc/identity/", views.kyc_profile_identify, name="document"),
]
