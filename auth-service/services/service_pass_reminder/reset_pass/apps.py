"""
Модуль конфигурации приложения для сброса пароля.

Этот модуль содержит класс `ResetPassConfig`, который используется
для настройки приложения, включая указание имени приложения.
"""

from django.apps import AppConfig


class ResetPassConfig(AppConfig):
    """
    Конфигурация для приложения `reset_pass`.

    Этот модуль содержит класс `ResetPassConfig`, который используется
    для настройки приложения, включая указание имени приложения.

    Атрибуты:
    - name (str): Имя приложения в формате "пакет.имя_приложения".
      В данном случае это "services.service_pass_reminder.reset_pass".
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "services.service_pass_reminder.reset_pass"
