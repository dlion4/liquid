from rest_framework import serializers
from .models import Message, Inbox
from amiribd.users.serializers import ProfileSerializer


class MessageSerializer(serializers.ModelSerializer):
    path_url = serializers.SerializerMethodField()
    sender = ProfileSerializer()
    receiver = ProfileSerializer()

    class Meta:
        model = Message
        fields = ["id", "path_url", "sender", "receiver"]

    def get_path_url(self, obj):
        return obj.get_absolute_url()


class InboxSerializer(serializers.ModelSerializer):
    message = MessageSerializer()

    class Meta:
        model = Inbox
        fields = "__all__"
