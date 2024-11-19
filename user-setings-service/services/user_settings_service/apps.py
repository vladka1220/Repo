from django.apps import AppConfig


class UserSettingsConfig(AppConfig):
    """
    Конфигурация приложения 'user_settings'.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "user_settings"
    verbose_name = "User Settings"  # Отображаемое имя приложения в админке
