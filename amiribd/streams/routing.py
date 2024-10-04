from django.urls import reverse, path, include
from amiribd.streams.notifications.news.routing import urlpatterns
from channels.routing import URLRouter

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
    # path('ws/notifications/test', AsyncTestNotificationConsumer.as_asgi()),
    # path('ws/notifications/posts', PostConsumer.as_asgi()),

    # the urls for the websocket connections

    # news urls
    path("ws/streams/news/", URLRouter(urlpatterns)), 

]
