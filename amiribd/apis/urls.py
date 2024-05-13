from django.urls import path

from amiribd.apis import views

app_name = "apis"
urlpatterns = [
    path("mpesa/callback", views.mpesa_callback_url, name="mpesa-callback"),
]
