import logging
from typing import Dict, Any
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import get_language
from rest_framework import serializers
from config.system_messages_config.error_messages import get_message
from .models import CustomUser


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Проверка, существует ли пользователь с данным email
        try:
            user = service_register_customuser.objects.get(email=value)
        except service_register_customuser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value
