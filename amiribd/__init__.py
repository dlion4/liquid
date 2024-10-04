__version__ = "0.1.0"
__version_info__ = tuple(
    int(num) if num.isdigit() else num
    for num in __version__.replace("-", ".", 1).split(".")
)

import redis
from asgiref.sync import sync_to_async, async_to_sync
from config.redis.utils import RedisInitialization, NotificationWebsocketClient
from channels.layers import get_channel_layer

redis_client = RedisInitialization()
notification_websocket_client = NotificationWebsocketClient()


# Get channel layer for sending notifications
# channel_layer = get_channel_layer()

# def listen_for_new_notifications():
#     r = redis.StrictRedis(host='localhost', port=6379, db=0)
#     while True:
#         notifications = r.brpop('notifications')
#         if notifications:
#             async_to_sync(channel_layer.group_send)(
#                 'test_notifications_group',
#                 {
#                     'type': 'send_notification',
#                     'message': notifications[1].decode('utf-8')
#                 }
#             )

# import threading
# threading.Thread(target=listen_for_new_notifications, daemon=True).start()
