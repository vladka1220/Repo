from django.apps import AppConfig


class MessagesConfig(AppConfig):
    """
    Конфигурация приложения 'messages'.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "messages"
    verbose_name = "Messages Service"
