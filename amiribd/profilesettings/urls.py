from django.urls import path, include

from . import views


app_name = "settings"

urlpatterns = [
    path(
        "notifications/",
        include("amiribd.profilesettings.htmx.urls"),
        name="notifications",
    ),
]
