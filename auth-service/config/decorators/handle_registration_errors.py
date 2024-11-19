"""
Модуль содержит декоратор для обработки ошибок регистрации.

Декоратор `handle_registration_errors` обрабатывает различные типы
исключений, возникающих при регистрации пользователя, и возвращает соответствующие
ответы с ошибками.
"""

import logging
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from config.system_messages_config.error_messages import get_message
from config.system_messages_config.error_codes import ERROR_CODES

logger = logging.getLogger(__name__)


class RegistrationError(Exception):
    """Общая ошибка регистрации."""


class UserCreationError(RegistrationError):
    """Ошибка, возникающая при создании пользователя."""


class EmailAlreadyRegisteredError(RegistrationError):
    """Ошибка, возникающая при попытке зарегистрировать уже существующий email."""


class InvalidEmailError(RegistrationError):
    """Ошибка, возникающая при недопустимом email."""


class EmailRequiredError(RegistrationError):
    """Ошибка, возникающая при отсутствии email."""


class PasswordRequiredError(RegistrationError):
    """Ошибка, возникающая при отсутствии пароля."""


class PasswordMismatchError(RegistrationError):
    """Ошибка, возникающая при несовпадении паролей."""


class PasswordMinLengthError(RegistrationError):
    """Ошибка, возникающая при недостаточной длине пароля."""


class PasswordMaxLengthError(RegistrationError):
    """Ошибка, возникающая при превышении максимальной длины пароля."""


def handle_registration_errors(view_func):
    """
    Декоратор для обработки ошибок регистрации в методах представления.

    Параметры:
    ----------
    view_func : callable
        Метод представления, который будет обернут декоратором.

    Возвращает:
    ----------
    callable
        Обернутый метод с обработкой ошибок регистрации.
    """

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except UserCreationError as e:
            logger.error("User creation error: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_400_BAD_REQUEST"],
                    "message": get_message("user_creation_error").format(error=str(e)),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except EmailAlreadyRegisteredError as e:
            logger.error("Email already registered: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_400_BAD_REQUEST"],
                    "message": get_message("email_already_registered"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidEmailError as e:
            logger.error("Invalid email: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_400_BAD_REQUEST"],
                    "message": get_message("email_invalid"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except EmailRequiredError as e:
            logger.error("Email required: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_400_BAD_REQUEST"],
                    "message": get_message("email_required"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except PasswordRequiredError as e:
            logger.error("Password required: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_400_BAD_REQUEST"],
                    "message": get_message("password_required"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except PasswordMismatchError as e:
            logger.error("Password mismatch: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_400_BAD_REQUEST"],
                    "message": get_message("password_mismatch"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except PasswordMinLengthError as e:
            logger.error("Password min length error: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_400_BAD_REQUEST"],
                    "message": get_message("password_min_length"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except PasswordMaxLengthError as e:
            logger.error("Password max length error: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_400_BAD_REQUEST"],
                    "message": get_message("password_max_length"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    return wrapper
