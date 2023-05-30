from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

# Cabinet serializers
from cabinet.models import TgUser, ProfileCard, Post


class TgUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TgUser
        fields = ["id", "username", "telegram"]


class UserRegistrationSerializer(BaseUserRegistrationSerializer):

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ["username", "telegram", "password"]


class ProfileCardSerializer(serializers.ModelSerializer):
    user = TgUserSerializer()

    class Meta:
        model = ProfileCard
        # fields = ["user", "name", "bio", "experience"]
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"
