from channels.generic.websocket import AsyncWebsocketConsumer
import json
from amiribd import redis_client
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class NotificationWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self, subprotocol=None, headers=None):
        self.group_name = "updates"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept(subprotocol, headers)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.close(code)

    async def receive(self, text_data):
        # data = json.loads(text_data)

        # event = {"type": "send_message", "message": data}

        # await self.send_message(event)
        pass

    # async def send_message(self, event):
    #     message = json.loads(event["message"])
    #     await self.send(message)

    async def send_update(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    @staticmethod
    def listen_to_redis():
        pubsub = redis_client.client.pubsub()

        pubsub.subscribe("posts_channel_kwasa")

        for message in pubsub.listen():
            async_to_sync(get_channel_layer().group_send)(
                "updates",{
                    "type": 'send_update',
                    "message":message['data']
                }
            )



    
from threading import Thread
Thread(target=NotificationWebsocketConsumer.listen_to_redis, daemon=True).start()