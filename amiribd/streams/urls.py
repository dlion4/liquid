from django.urls import path
from . import views


app_name = "streams"

urlpatterns = [
    path("<slug:room_slug>/", views.RoomView.as_view(), name="room-detail"),
    path(
        "network/hello/",
        views.create_retrieve_message,
        name="hello",
    ),
    path(
        "network/create-retrieve-message/",
        views.MessageInboxRetrieveCreateView.as_view(),
        name="message_create_retrieve_inbox",
    ),
    path(
        "message/<int:pk>/<receiver>/",
        views.MessageInboxView.as_view(),
        name="message-detail",
    ),
]
