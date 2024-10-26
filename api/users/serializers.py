from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()




class UserRegistrationSerializer(serializers.Serializer):
    email  = serializers.EmailField()
    username = serializers.CharField(max_length=150)

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
        )
        user.save()
        return user
