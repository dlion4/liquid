from django.urls import path

from . import views


app_name = "profile"

urlpatterns = [
    path("", views.ProfileView.as_view(), name="profile"),
    path("obtain-token/", views.ObtainTokenView.as_view(), name="obtain-token"),
    path("verify-token/", views.TokenVerifyView.as_view(), name="verify-token"),
    path("revoke-token/", views.TokenRevokeView.as_view(), name="revoke-token"),
    path("refresh-token/<user_id>/", views.RefreshTokenView.as_view(), name="refresh-token"),
    path(
        "notifications/",
        views.ProfileNotificationView.as_view(),
        name="notifications",
    ),
    path(
        "account-activity/",
        views.ProfileAccountActivityView.as_view(),
        name="account-activity",
    ),
    path(
        "security-settings/",
        views.ProfileSecuritySettingView.as_view(),
        name="security-settings",
    ),
    path(
        "social-connected/",
        views.ProfileSocialConnectedView.as_view(),
        name="social-connected",
    ),
]
