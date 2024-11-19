"""
Включает маршруты для сервиса настроек пользователя.
"""

from django.urls import path, include

# Общие на сервис URL конфигурации
urlpatterns = [
    # Маршруты для сервиса настроек пользователя
    path("meerkat_api/user_settings/", include("user_settings.urls")),
]
