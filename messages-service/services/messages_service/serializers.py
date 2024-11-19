from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.Serializer):
    """
    Сериализатор для модели Message, который используется для валидации и преобразования данных.

    Методы:
        create(): Создание нового сообщения.
        update(): Обновление существующего сообщения.
    """

    id = serializers.CharField(read_only=True)
    sender = serializers.CharField(required=True)
    recipient = serializers.CharField(required=True)
    content = serializers.CharField(required=True)
    timestamp = serializers.DateTimeField()

    def create(self, validated_data):
        """
        Создание нового объекта Message.

        Args:
            validated_data (dict): Проверенные данные для создания сообщения.

        Returns:
            Message: Созданный объект сообщения.
        """
        message = Message(**validated_data)
        message.save()
        return message

    def update(self, instance, validated_data):
        """
        Обновление существующего объекта Message.

        Args:
            instance (Message): Существующий объект сообщения.
            validated_data (dict): Проверенные данные для обновления сообщения.

        Returns:
            Message: Обновленный объект сообщения.
        """
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
