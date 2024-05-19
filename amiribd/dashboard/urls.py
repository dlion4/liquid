from django.urls import path, include
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="home"),
    path("welcome/", views.welcome, name="welcome"),
    path("invest/", include("amiribd.invest.urls", namespace="invest")),
    path("support/", views.support, name="support"),
    path("streams/", include("amiribd.streams.urls", namespace="streams")),
    path("blogging/", include("amiribd.articles.urls", namespace="articles")),
]
