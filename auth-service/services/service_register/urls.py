"""
URL конфигурация для приложения регистрации пользователей.

Этот модуль определяет маршруты для регистрации нового пользователя.

Маршрут:
- `""` (пустой маршрут): Обрабатывает POST-запросы
для регистрации пользователя.

Имя маршрута — `user-register`.
"""

from django.urls import path
from .views import UserRegistrationView

app_name = "services.service_register"

urlpatterns = [
    path("", UserRegistrationView.as_view(), name="user_register"),
]
