from amiribd.users.serializers import ProfileSerializer, UserSerializer
from amiribd.posts.models import Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "author",
            "date_posted",
        ]
