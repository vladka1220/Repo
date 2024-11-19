from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet

# Создание маршрутизатора для API
router = DefaultRouter()
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls)),
]
