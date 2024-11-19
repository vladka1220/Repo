"""
Модуль конфигурации приложения для регистрации пользователей.

Этот модуль содержит класс `ServiceRegisterConfig`, который используется
для настройки приложения, включая указание имени и типа поля по умолчанию
для автоинкрементных полей.
"""

from django.apps import AppConfig


class ServiceRegisterConfig(AppConfig):
    """
    Конфигурация для приложения `service_register`.

    Этот модуль содержит класс `ServiceRegisterConfig`, который используется
    для настройки приложения, включая указание имени приложения.

    Атрибуты:
    - name (str): Имя приложения в формате "пакет.имя_приложения".
      В данном случае это "services.service_register".
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "services.service_register"
