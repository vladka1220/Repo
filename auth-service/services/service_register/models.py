"""
Модель данных для регистрации пользователей.

Эта модель наследует стандартную модель AbstractUser, предоставляемую Django.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя, расширяющая стандартную модель AbstractUser.

    Attributes:
        is_new_user (bool): Флаг, указывающий, является ли пользователь новым.
        Значение по умолчанию — True.
    """

    is_new_user = models.BooleanField(default=True)

    class Meta:
        """
        Метаданные модели.

        Attributes:
            app_label (str): Название приложения.
        """

        app_label = "service_register"

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта пользователя.

        Returns:
            str: Имя пользователя.
        """
        return str(self.username) if self.username else ""
