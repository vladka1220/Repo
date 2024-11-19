"""
Включает маршруты для сервиса вики.
"""

from django.urls import path, include

# Общие на сервис URL конфигурации
urlpatterns = [
    # Маршруты для сервиса вики
    path(
        "meerkat_api/wiki_service/",
        include("services.urls", namespace="services"),
    ),
]
