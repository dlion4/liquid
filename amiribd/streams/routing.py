from django.urls import reverse, path


from .consumers import StreamRoomConsumer


websocker_urlpatterns = [
    path("ws/streams/<room_slug>", StreamRoomConsumer.as_asgi()),
]

