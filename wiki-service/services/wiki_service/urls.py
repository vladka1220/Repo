from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WikiPageViewSet

router = DefaultRouter()
router.register(r"pages", WikiPageViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
