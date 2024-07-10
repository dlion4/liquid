import json
import redis
from django.conf import settings
from datetime import timedelta, datetime
from typing import Any, List
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class RedisInitialization:
    """
    This is a custom redis client object fro most of the asynchronous 
    task that will need to be performaded and need quick retrieval
    """

    def __init__(self, **kwargs)-> None:
        """"
        This method intialize the redis client and provide the 
        redis client for the addition of the object to the redis server
        and the retrieveal of the object from the redis server
        It uses the dfault ddjango db as its database

        ### setup:
         - redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
        """
        self.client = redis.StrictRedis(
            host=settings.REDIS_HOST, 
            port=settings.REDIS_PORT, 
            db=settings.REDIS_DB,
            decode_responses=settings.REDIS_DECODE_RESPONSE,
            ssl=settings.REDIS_SSL,
            ssl_cert_reqs=settings.REDIS_SSL_CERT_REQUIRED,
        )

    def upload_instance_to_redis(
        self, 
        instance_id:str, 
        instance_data:dict[str, Any]={},
        instance_name:str='instance', 
        expiry:datetime=timedelta(minutes=5),
        channel_name:str|None=None, 
    )->None:
        """
        Add item to the redis server using the instance_id
        This id is needed for the retrieval of the instance data

        ### Broad casting data and messages
        - if the channel_name is provided then call the broadcasting mesage
        ---------------------------------------------------------------------
        if channel_name is not None:
            publish_instance_to_redis_channels(
            channel=channel_name,
            data=instance_data
            )
        """
        instance_key = f"{instance_name}:{instance_id}"
        self.client.setex(name=instance_key, time=expiry, value=json.dumps(instance_data))
        
        if channel_name is not None:
            self.publish_instance_to_redis_channels(
                channel_name,
                # the instance data has been convered to the jsons items that can tbe sent over to the
                # network by json format
                instance_data
            )

    def retrieve_instance_from_redis(self, instance_name:str='instance')->List[dict[str, Any]]:
        """Based on the provided key to the redis server returned the saved keys"""
        instance_key = f'{instance_name}'
        instance_data = json.loads(self.client.get(instance_key))
        return instance_data
    
    def publish_instance_to_redis_channels(self, channel:str, data:dict[str, Any]={})->None:
        """
        This method publishes instance data to the reids server 
        So that those subscribed to this cahnnel can receive the messages 
        Or the data in realtime onece the message has been braodcasted onto the channel
        redis_clients = self.client.publish(channel=channel_name, data=data)
        """
        self.client.publish(channel, json.dumps(data))


class NotificationWebsocketClient:
    """
    This class is responsible for sending notifications over websockets.
    It uses Django Channels to send messages to the websocket clients.
    """

    def __init__(self)->None:
        """
        Initialize the websocket client with the instance_id for retrieving data from Redis
        """
        self.redis_client = RedisInitialization()

    def send_notification(
        self,
        notification_group: str, 
        message:str ,
        redis_instance_id:int|None=None,
        redis_instance_name:str|None=None, 
    )->None:
        """
        Send a notification to all websocket clients.
        - If redis_instance_id and redis_instance_name are None : The notification was sent not via redis
        - If redis_instance_id and redis_instance_name are provided : The notification was sent via redis
        -------------------------------------------------------------------------------------------------
        The message and the group cant be null 
        The notification is sent to the group defined in the settings.
            channel_layer = get_channel_layer()
            await async_to_sync(channel_layer.group_send)(
                settings.NOTIFICATION_GROUP,
                {
                    'type': 'notification',
                    'notification_type': notification_type,
                    'message': message,
                    'instance_id': self.instance_id
                }
            )
        """
        if self.retrieve_redis_message(redis_instance_id, redis_instance_name):
            message =  self.retrieve_redis_message(redis_instance_id, redis_instance_name)
        message = message
        # print(f"Sending notification to {notification_group}: {message}")
        # Send notification to WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'{notification_group}',
            {
                'type': 'send_notification',
                'message': f"{json.dumps(message)}"
            }
        )

    def retrieve_redis_message(
        self,  
        redis_instance_id:int|None=None,
        redis_instance_name:str|None=None, 
    )->List[dict[str, Any]]|None:
        
        """
        This function has to retun the redis message therefore has 
        to have the instanceid and the name
        """
        message_key = f"{redis_instance_name}:{redis_instance_id}"
        message =  self.redis_client.retrieve_instance_from_redis(message_key)
        return message
    


