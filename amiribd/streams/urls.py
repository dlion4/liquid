from django.urls import path
from . import views


app_name = "streams"

urlpatterns = [
    path("<slug:room_slug>/", views.RoomView.as_view(), name="room-detail"),
    path(
        "create-retrieve-message/",
        views.create_retrieve_message,
        name="message-create-retrieve-inbox",
    ),
]
