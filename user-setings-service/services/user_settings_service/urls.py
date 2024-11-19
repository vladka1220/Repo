from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserSettingViewSet

router = DefaultRouter()
router.register(r"settings", UserSettingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

"""
URL-конфигурация для приложения `user_settings`.

Использует DefaultRouter для автоматического создания URL-ов для `UserSettingViewSet`.
"""
