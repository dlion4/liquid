import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from amiribd.streams.models import Room, RoomMessage
from django.template.loader import render_to_string


class StreamRoomConsumer(WebsocketConsumer):
    def connect(self):

        # self.room_name = self.scope["url_route"]["kwargs"]["room_slug"]
        # self.room_group_name = "stream_%s" % self.room_name

        # # Join room group
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name, self.channel_name
        # )

        self.profile = self.scope["user"].profile_user
        self.room_name_slug = self.scope["url_route"]["kwargs"]["room_slug"]

        self.room = get_object_or_404(Room, slug=self.room_name_slug)

        self.accept()

    def receive(self, text_data):
        # data = json.loads(text_data)

        print(text_data)
        if text_data:
            message = RoomMessage.objects.create(
                room=self.room, profile=self.profile, message=text_data
            )
        html_message = render_to_string(
            "account/dashboard/v1/chats/messages.html",
            context={"message": message},
        )
        self.send(text_data=html_message)
