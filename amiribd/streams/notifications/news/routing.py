from django.urls import path

from .consumers import (
    NotificationWebsocketConsumer
)

urlpatterns = [
    path("notifications", NotificationWebsocketConsumer.as_asgi()), # path=ws/streams/news/notification
]