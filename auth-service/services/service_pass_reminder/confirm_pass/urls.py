"""
Содержит маршруты для подтверждения сброса пароля.
"""

# Импорт из стандартной библиотеки
from django.urls import path

# Локальные импорты
from . import views

app_name = "confirm_pass"

urlpatterns = [
    path("request/", views.PasswordResetConfirmView.as_view(), name="request"),
    path(
        "confirm/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="confirm_pass",
    ),
]
