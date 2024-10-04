from amiribd import redis_client
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .serializers import PostSerializer


@receiver(post_save, sender=Post)
def publish_posts(sender, instance, **kwargs):
    """
    ## Broadcast Post on save
     -Set the key item to reis and then braodcast the data to the channel
    ----------------------------------------------------------------------
    ### Steps
        - Serialize the created data (post in this case)
            -- post_data = PostSerializer(instance=instance).data
        - Set the data to the redis client

            redis_client.upload_instance_to_redis(
                instance_id=instance.pk,
                instance_data=post_data,
                instance_name="posts",
                channel_name="posts_channel_kwasa",
            )
        - publish the data to the reis channel

        - The message is then boraidcasted 

        - will use axios in this case for the frontent
    """
    
    post_data = PostSerializer(instance=instance).data
    
    redis_client.upload_instance_to_redis(
        instance_id=instance.pk,
        instance_data=post_data, # get picked to be sent to the canel as thedata to be braodcasted | if not chanle_name then the data is just saved on toe the 
        instance_name="posts",
        # this line will enable use to publish this to the redis chanel for message
        channel_name="posts_channel_kwasa",
    )



