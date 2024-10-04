from django.urls import path, include
from . import views


app_name = "async"

urlpatterns = [
    path(
        "profile-register-vip-level/<int:vip_position_choice_id>/",
        views.ProfileRegisterVipLevelView.as_view(),
        name="profile-register-vip-level",
    ),
    path(
        "profile-filter-agent/",
        views.ProfileFilterAgentView.as_view(),
        name="profile-filter-agent",
    ),
    path(
        "profile-agent-plantform-selection/<int:platform_type_id>/",
        views.ProfileAgentPlantFormSelectionView.as_view(),
        name="profile-agent-plantorm-selection",
    ),
    path(
        "profile-agent-plantform-selection/",
        views.ProfileAgentPlantFormSelectionView.as_view(),
        name="profile-agent-plantorm-selection",
    ),
    path(
        "profile-filter-agent-platform/",
        views.ProfileFilterAgentPlatformView.as_view(),
        name="profile-filter-agent-platform",
    ),
]
