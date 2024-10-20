from django.urls import path

from . import views

app_name = "jobs"


urlpatterns = [
    path("applications/<job_id>/<applicant_id>",
        views.job_application_view,
        name="application_view"),
]
