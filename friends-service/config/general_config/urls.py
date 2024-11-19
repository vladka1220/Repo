"""
Определяет маршруты URL для проекта Django.

Включает маршруты для административного интерфейса, OAuth2 провайдера,
аутентификации через Keycloak и другие URL-адреса.
"""

from django.urls import path, include


urlpatterns = [
    path(
        "meerkat_api/friends/",
        include(("services.service_friends.urls", "services.service_friends")),
    ),
]
