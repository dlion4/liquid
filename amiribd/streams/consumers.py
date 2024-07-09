import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from amiribd.streams.models import Inbox, Room, RoomMessage
from django.template.loader import render_to_string
from channels.db import database_sync_to_async
from amiribd.streams.models import Message
from amiribd.streams.serializers import InboxSerializer, MessageSerializer
import logging

logger = logging.getLogger(__name__)


class StreamRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.room_name_slug = self.scope["url_route"]["kwargs"]["room_slug"]
        self.room_group_name = f"stream_{self.room_name_slug}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.close(code)

    async def receive(self, text_data):
        data = json.loads(text_data)
        event = {"type": "send_message", "message": data}

        print(data)

        await self.channel_layer.group_send(self.room_group_name, event)

    async def send_message(self, event):
        data = event["message"]

        # return the function that will create the room message

        response = {
            "message": data["message"],
            "sender": data["sender"],
        }

        await self.send(text_data=json.dumps({"message": response}))


class StreamPrivateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.message_pk = self.scope["url_route"]["kwargs"]["pk"]
        self.room_name = f"room_{self.message_pk}"

        # add the room to channels layers
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name,
        )

        self.close(code)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        event = {"type": "send_message", "message": data}

        await self.channel_layer.group_send(
            self.room_name,
            event,
        )

    async def send_message(self, event):
        data = event["message"]
        inbox_data = await self.create_message(data=data)

        response = {
            "sender": data["sender"],
            "message": data["message"],
            "inbox": inbox_data,
        }

        await self.send(text_data=json.dumps({"message": response}))

    @database_sync_to_async
    def create_message(self, data):
        # message object before starting to create inboxes

        message_obj = get_object_or_404(Message, pk=self.message_pk)
        return InboxSerializer(
            Inbox.objects.create(message=message_obj, body=data["message"])
        ).data


class AsyncStreamSupportConsumer(AsyncWebsocketConsumer):

    async def connet(self):
        self.support_number = self.scope["url_route"]["kwargs"]["profile_id"]
        await self.accept()

    async def disconnect(self, code):
        await self.close(code)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        event = {"type": "send_message", "message": data}

        await self.send_message(event)

    async def send_message(self, event):
        data = event["message"]

        response = {
            "sender": data["sender"],
            "receiver": data["receiver"],
            "message": data["message"],
        }

        await self.send(text_data=json.dumps({"message": response}))

