from rest_framework import viewsets, permissions
from .models import UserSetting
from .serializers import UserSettingSerializer


class UserSettingViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с настройками пользователя.

    Методы:
    - list: Возвращает настройки текущего пользователя.
    - create: Создает настройку для текущего пользователя.
    - retrieve, update, destroy: Операции для одной настройки.

    Атрибуты:
    - queryset: Все настройки пользователей.
    - serializer_class: Сериализатор для модели UserSetting.
    - permission_classes: Требует аутентификации.
    """

    queryset = UserSetting.objects.all()
    serializer_class = UserSettingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает настройки только для текущего аутентифицированного пользователя.
        """
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Устанавливает текущего пользователя при создании новой настройки.
        """
        serializer.save(user=self.request.user)
