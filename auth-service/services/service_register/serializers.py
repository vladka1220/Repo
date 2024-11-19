import logging
from typing import Dict, Any
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import requests
from config.system_messages_config.error_messages import get_message
from config.system_messages_config.error_codes import ERROR_CODES
from .models import CustomUser

logger = logging.getLogger(__name__)


class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "email",
            "password",
            "password_confirmation",
            "is_new_user",
        )
        read_only_fields = ["is_new_user", "id"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        password = attrs.get("password")
        password_confirmation = attrs.get("password_confirmation")
        email = attrs.get("email")

        if password != password_confirmation:
            raise ValidationError(
                {"password_confirmation": [get_message("password_mismatch")]},
                code=ERROR_CODES["HTTP_400_BAD_REQUEST"],
            )

        if isinstance(email, str) and email:
            if self.email_exists_in_keycloak(email):
                raise ValidationError(
                    {"email": [get_message("email_already_registered")]},
                    code=ERROR_CODES["HTTP_409_CONFLICT"],
                )
        else:
            raise ValidationError(
                {"email": [get_message("invalid_email")]},
                code=ERROR_CODES["HTTP_400_BAD_REQUEST"],
            )

        return attrs

    def create(self, validated_data: Dict[str, Any]) -> dict:
        password = validated_data.pop("password")
        validated_data.pop("password_confirmation")

        # Запрашиваем токен
        token = self.get_keycloak_token()

        keycloak_user_data = {
            "username": validated_data["email"],
            "email": validated_data["email"],
            "firstName": validated_data["first_name"],
            "enabled": True,
            "credentials": [
                {"type": "password", "value": password, "temporary": False}
            ],
        }

        try:
            user_id = self.create_keycloak_user(keycloak_user_data, token)

            # Репликация данных в профильный сервис
            profile_data = {
                "id": user_id,  # ID пользователя в Keycloak
                "username": validated_data["email"],
                "first_name": validated_data["first_name"],
                "email": validated_data["email"],
            }

            # Вызываем метод репликации
            self.replicate_user_profile_to_django(profile_data, token)

            # Отправляем email для верификации
            url = f"{settings.KEYCLOAK_CONFIG['KEYCLOAK_SERVER_URL']}/admin/realms/{settings.KEYCLOAK_CONFIG['KEYCLOAK_REALM']}/users/{user_id}/execute-actions-email"
            params = {
                "client_id": settings.KEYCLOAK_CONFIG["KEYCLOAK_CLIENT_ID"],
                "redirect_uri": settings.KEYCLOAK_CONFIG["KEYCLOAK_REDIRECT_URI"],
                "client_secret": settings.KEYCLOAK_CONFIG["KEYCLOAK_CLIENT_SECRET_KEY"],
            }
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
            body = ["VERIFY_EMAIL"]

            response = requests.put(
                url, params=params, json=body, headers=headers, timeout=10
            )
            if response.status_code == 204:
                logger.info("Verification email sent successfully.")
            else:
                logger.error("Error sending verification email: %s", response.text)
                raise ValidationError("Не удалось отправить верификационный email.")

        except requests.RequestException as e:
            logger.error("Сетевая ошибка при отправке email: %s", e)
            raise ValidationError("Ошибка сети. Попробуйте позже.")

        except Exception as e:
            logger.error("Ошибка при создании пользователя или отправке email: %s", e)
            raise ValidationError("Произошла ошибка. Попробуйте позже.")

        return validated_data

    def get_keycloak_token(self) -> str:
        """Запрос токена от Keycloak"""
        url = f"{settings.KEYCLOAK_CONFIG['KEYCLOAK_SERVER_URL']}/realms/{settings.KEYCLOAK_CONFIG['KEYCLOAK_REALM']}/protocol/openid-connect/token"

        data = {
            "client_id": settings.KEYCLOAK_CONFIG["KEYCLOAK_CLIENT_ID"],
            "client_secret": settings.KEYCLOAK_CONFIG["KEYCLOAK_CLIENT_SECRET_KEY"],
            "grant_type": "client_credentials",
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 200:
            token_data = response.json()
            return token_data["access_token"]
        else:
            raise Exception(
                f"Failed to get token: {response.status_code}, {response.text}"
            )

    def create_keycloak_user(self, user_data: Dict[str, Any], token: str) -> str:
        """Создание пользователя в Keycloak с использованием токена"""
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        url = f"{settings.KEYCLOAK_CONFIG['KEYCLOAK_SERVER_URL']}/admin/realms/{settings.KEYCLOAK_CONFIG['KEYCLOAK_REALM']}/users"

        response = requests.post(url, json=user_data, headers=headers)

        if response.status_code == 201:
            return response.headers["Location"].split("/")[-1]  # ID пользователя
        else:
            logger.error("Ошибка создания пользователя: %s", response.text)
            raise Exception(
                f"Failed to create user: {response.status_code}, {response.text}"
            )

    def email_exists_in_keycloak(self, email: str) -> bool:
        """Проверка, существует ли email в Keycloak"""
        token = self.get_keycloak_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        url = f"{settings.KEYCLOAK_CONFIG['KEYCLOAK_SERVER_URL']}/admin/realms/{settings.KEYCLOAK_CONFIG['KEYCLOAK_REALM']}/users"
        params = {"email": email}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            users = response.json()
            return len(users) > 0
        else:
            logger.error("Ошибка при получении пользователей: %s", response.text)
            return False

    def replicate_user_profile_to_django(
        self, user_data: dict, access_token: str
    ) -> None:
        profile_service_url = f"{settings.PROFILE_SERVICE_URL}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                profile_service_url, json=user_data, headers=headers
            )

            if response.status_code != 201:
                logger.error("Ошибка при репликации профиля: %s", response.text)
                raise Exception(
                    f"Failed to replicate profile data: {response.status_code}, {response.text}"
                )
        except requests.exceptions.RequestException as exc:
            logger.error("Ошибка запроса к сервису профиля: %s", str(exc))
            raise Exception(f"Request to profile service failed: {str(exc)}")
