from django.urls import reverse, path

from . import views

app_name = "notifications"
urlpatterns = [
    path(
        "notifications-subscribe/<notification_id>/<notification_type_id>/<profile_id>/",
        views.HandleNotificationSwitcherView.as_view(),
        name="notifications-subscribe",
    ),
    path(
        "subscribe/",
        views.ProfileNotificationSubscribeLookupView.as_view(),
        name="notifications-subscribe-lookup",
    ),
]
