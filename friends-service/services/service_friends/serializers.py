from rest_framework import serializers
from .models import Friend, FriendRequest, FavoriteUser
from django.contrib.auth.models import User


class FriendSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Friend.
    """

    friend_username = serializers.CharField(source="friend.username")  # Имя друга

    class Meta:
        model = Friend
        fields = ["friend_username", "created_at"]  # Поля для сериализации


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    """

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]  # Поля для сериализации


class FavoriteUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели FavoriteUser.
    """

    favorite_username = serializers.CharField(
        source="favorite.username"
    )  # Имя избранного пользователя

    class Meta:
        model = FavoriteUser
        fields = ["favorite_username", "created_at"]  # Поля для сериализации


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели FriendRequest.
    """

    from_username = serializers.CharField(
        source="from_user.username"
    )  # Имя отправителя
    to_username = serializers.CharField(source="to_user.username")  # Имя получателя

    class Meta:
        model = FriendRequest
        fields = [
            "from_username",
            "to_username",
            "created_at",
            "is_accepted",
        ]  # Поля для сериализации


class FriendProfileSerializer(serializers.Serializer):
    """
    Сериализация ответа сервиса Profile для получения списка друзей по айди
    """

    id = serializers.IntegerField()  # 'id' is an integer field
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255, allow_blank=True)
    avatar = serializers.URLField(allow_null=True, required=False)
    specializations = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )
