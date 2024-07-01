from .models import User, Profile
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "verified")


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    name_initials = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [f.name for f in Profile._meta.fields] + ["name_initials", "image_url"]

    def get_name_initials(self, obj):
        return obj.generate_initials()
    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None
