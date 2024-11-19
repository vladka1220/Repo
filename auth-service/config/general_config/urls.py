"""
Включает маршруты для сервиса аутентификации и регистрации пользователей.
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Общие на сервис URL конфигурации
urlpatterns = [
    # Маршруты для сервиса аутентификации
    path(
        "meerkat_api/auth/",
        include("services.service_auth.urls", namespace="services.service_auth"),
    ),
    # Маршруты для сервиса регистрации
    path(
        "meerkat_api/reg/",
        include(
            "services.service_register.urls", namespace="services.service_register"
        ),
    ),
    # Маршруты для сброса пароля
    path(
        "meerkat_api/reset_pass/",
        include(
            "services.service_pass_reminder.reset_pass.urls",
            namespace="services.service_pass_reminder.reset_pass",
        ),
    ),
    # Маршруты для подтверждения пароля
    path(
        "meerkat_api/confirm_pass/",
        include(
            "services.service_pass_reminder.confirm_pass.urls",
            namespace="services.service_pass_reminder.confirm_pass",
        ),
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
