"""
Модуль содержит декоратор для обработки ошибок аутентификации.

Декоратор `handle_authentication_errors` обрабатывает различные типы
исключений, возникающих при аутентификации пользователя, и возвращает соответствующие
ответы с ошибками.
"""

import logging
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from config.system_messages_config.error_messages import get_message
from config.system_messages_config.error_codes import ERROR_CODES

logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Общая ошибка аутентификации."""


class InvalidCredentialsError(AuthenticationError):
    """Ошибка, возникающая при вводе неверных учетных данных."""


class AccountLockedError(AuthenticationError):
    """Ошибка, возникающая при блокировке учетной записи."""


class AccountInactiveError(AuthenticationError):
    """Ошибка, возникающая при неактивной учетной записи."""


class PasswordExpiredError(AuthenticationError):
    """Ошибка, возникающая при истечении срока действия пароля."""


class AuthenticationRequiredError(AuthenticationError):
    """Ошибка, возникающая при отсутствии необходимой аутентификации."""


def handle_auth_errors(view_func):
    """
    Декоратор для обработки ошибок аутентификации в методах представления.

    Параметры:
    ----------
    view_func : callable
        Метод представления, который будет обернут декоратором.

    Возвращает:
    ----------
    callable
        Обернутый метод с обработкой ошибок аутентификации.
    """

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except InvalidCredentialsError as e:
            logger.error("Invalid credentials: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_401_UNAUTHORIZED"],
                    "message": get_message("invalid_credentials"),
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except AccountLockedError as e:
            logger.error("Account locked: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_403_FORBIDDEN"],
                    "message": get_message("account_locked"),
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        except AccountInactiveError as e:
            logger.error("Account inactive: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_403_FORBIDDEN"],
                    "message": get_message("account_inactive"),
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        except PasswordExpiredError as e:
            logger.error("Password expired: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_401_UNAUTHORIZED"],
                    "message": get_message("password_expired"),
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except AuthenticationRequiredError as e:
            logger.error("Authentication required: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_401_UNAUTHORIZED"],
                    "message": get_message("authentication_required"),
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

    return wrapper
