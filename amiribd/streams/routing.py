from django.urls import reverse, path


from .consumers import (
    StreamRoomConsumer,
    StreamPrivateConsumer,
    AsyncStreamSupportConsumer,
)


websocket_urlpatterns = [
    path("ws/streams/<room_slug>", StreamRoomConsumer.as_asgi()),
    path("ws/streams/private/<int:pk>", StreamPrivateConsumer.as_asgi()),
    # support streams
    path("ws/streams/support/<profile_id>", AsyncStreamSupportConsumer.as_asgi()),
]
