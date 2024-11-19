from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Message
from .serializers import MessageSerializer
from mongoengine.errors import DoesNotExist


class MessageViewSet(viewsets.ViewSet):
    """
    ViewSet для управления сообщениями.

    Методы:
        list(): Получение списка всех сообщений.
        retrieve(): Получение отдельного сообщения по идентификатору.
        create(): Создание нового сообщения.
        update(): Обновление существующего сообщения.
        destroy(): Удаление сообщения.
    """

    def list(self, request):
        """
        Получение списка всех сообщений.
        """
        messages = Message.__objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Получение отдельного сообщения по идентификатору.
        """
        try:
            message = Message.__objects.get(id=pk)
        except DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def create(self, request):
        """
        Создание нового сообщения.
        """
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Обновление существующего сообщения.
        """
        try:
            message = Message.__objects.get(id=pk)
        except DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Удаление сообщения.
        """
        try:
            message = Message.__objects.get(id=pk)
        except DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
