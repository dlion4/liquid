from django.urls import path


app_name = "ai"

from . import views

urlpatterns = [
    path("", views.AIGenerateContentView.as_view(), name="generate"),
]
