from django.urls import path

from . import views

app_name = "ai"


urlpatterns = [
    path("", views.AIGenerateContentView.as_view(), name="generate"),
]
