from django.urls import reverse, path


from .consumers import StreamRoomConsumer, StreamPrivateConsumer


websocket_urlpatterns = [
    path("ws/streams/<room_slug>", StreamRoomConsumer.as_asgi()),
    path("ws/streams/private/<int:pk>", StreamPrivateConsumer.as_asgi()),
]
