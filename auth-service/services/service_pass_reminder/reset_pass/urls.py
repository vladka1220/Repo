"""
Содержит маршруты для сброса пароля пользователей.
"""

from django.urls import path
from . import views

app_name = "reset_pass"

urlpatterns = [
    path("request/", views.PasswordResetRequestView.as_view(), name="request"),
    path(
        "confirm/<uidb64>/<token>/",
        views.PasswordResetRequestView.as_view(),
        name="reset_pass",
    ),
]
