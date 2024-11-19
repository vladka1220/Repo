from django.urls import path, include

urlpatterns = [
    path("meerkat_api/messages_service", include("messages.urls")),
]
