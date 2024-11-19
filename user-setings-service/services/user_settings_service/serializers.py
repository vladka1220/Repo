from rest_framework import serializers
from .models import UserSetting


class UserSettingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели `UserSetting`. Преобразует модель в JSON и обратно.

    Поля:
    - id (только для чтения)
    - user (только для чтения)
    - key
    - value
    """

    class Meta:
        model = UserSetting
        fields = ["id", "user", "key", "value"]
        read_only_fields = ["id", "user"]
