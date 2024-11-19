"""
Модуль содержит декоратор для обработки успешных сообщений.

Декоратор `handle_success_messages` обрабатывает различные статусы ответов
и возвращает соответствующие сообщения об успехе.
"""

import logging
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from config.system_messages_config.error_messages import get_message

logger = logging.getLogger(__name__)


class SuccessMessage:
    """Общая база для сообщений об успешных операциях."""

    def __init__(self, message: str):
        self.message = message


class RegistrationSuccess(SuccessMessage):
    """Сообщение о успешной регистрации."""

    def __init__(self):
        super().__init__(get_message("registration_successful"))


class EmailConfirmationSent(SuccessMessage):
    """Сообщение о том, что письмо для подтверждения было отправлено."""

    def __init__(self, email: str):
        super().__init__(get_message("email_confirmation_sent").format(email=email))


class PasswordUpdated(SuccessMessage):
    """Сообщение о том, что пароль был успешно обновлён."""

    def __init__(self):
        super().__init__(get_message("password_updated"))


def handle_success_messages(view_func):
    """
    Декоратор для обработки успешных сообщений в методах представления.

    Параметры:
    ----------
    view_func : callable
        Метод представления, который будет обернут декоратором.

    Возвращает:
    ----------
    callable
        Обернутый метод с обработкой успешных сообщений.
    """

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        response = view_func(*args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            message = RegistrationSuccess()
            logger.info("Success: %s", message.message)
            return Response(
                {
                    "status": status.HTTP_201_CREATED,
                    "message": message.message,
                    "data": response.data,
                },
                status=status.HTTP_201_CREATED,
            )

        if response.status_code == status.HTTP_202_ACCEPTED:
            email = str(kwargs.get("email", ""))
            message = EmailConfirmationSent(email)
            logger.info("Success: %s", message.message)
            return Response(
                {
                    "status": status.HTTP_202_ACCEPTED,
                    "message": message.message,
                },
                status=status.HTTP_202_ACCEPTED,
            )

        if response.status_code == status.HTTP_200_OK:
            message = PasswordUpdated()
            logger.info("Success: %s", message.message)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": message.message,
                    "data": response.data,
                },
                status=status.HTTP_200_OK,
            )

        return response  # Возврат оригинального ответа для других случаев

    return wrapper
