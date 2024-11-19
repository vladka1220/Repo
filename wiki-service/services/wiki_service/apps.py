from django.apps import AppConfig


class WikiSettingsConfig(AppConfig):
    """
    Конфигурация приложения 'wiki'.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "wiki_service"
    verbose_name = "Wiki Service"  # Отображаемое имя приложения в админке
