from django.urls import path,reverse

from . import views


app_name = "kyc-htmx-validation"

urlpatterns = [
    path("validate-unique-phone-number/", views.ValidateUniquePhoneNumberView.as_view(), name="validate-unique-phone-number"),
    path("validate-date-of-birth/", views.ValidatedObValidView.as_view(), name="validate-date-of-birth"),
]
