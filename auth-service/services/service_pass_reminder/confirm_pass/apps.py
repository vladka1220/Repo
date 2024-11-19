"""
Модуль конфигурации приложения для подтверждения пароля.

Этот модуль содержит класс `ConfirmPassConfig`, который используется
для настройки приложения, включая указание имени приложения.
"""

from django.apps import AppConfig


class ConfirmPassConfig(AppConfig):
    """
    Конфигурация для приложения `confirm_pass`.

    Этот модуль содержит класс `ConfirmPassConfig`, который используется
    для настройки приложения, включая указание имени приложения.

    Атрибуты:
    - name (str): Имя приложения в формате "пакет.имя_приложения".
      В данном случае это "services.service_pass_reminder.confirm_pass".
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "services.service_pass_reminder.confirm_pass"
