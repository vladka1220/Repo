from django.contrib.auth.models import User
from django.db import models


class UserSetting(models.Model):
    """
    Модель для хранения настроек пользователя.

    Поля:
    - user (ForeignKey): Пользователь, к которому относятся настройки.
    - key (CharField): Ключ настройки.
    - value (TextField): Значение настройки.

    Метаданные:
    - unique_together: Обеспечивает уникальность сочетания пользователя и ключа.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        unique_together = ("user", "key")

    def __str__(self):
        """
        Возвращает строковое представление объекта.

        Формат: '<username>: <key> = <value>'
        """
        return f"{self.user.username}: {self.key} = {self.value}"
