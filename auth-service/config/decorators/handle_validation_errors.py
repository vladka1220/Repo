"""
Модуль содержит декоратор для обработки ошибок валидации.

Декоратор `handle_validation_errors` обрабатывает различные типы
исключений, возникающих при валидации данных, и возвращает соответствующие
ответы с ошибками.
"""

import logging
from functools import wraps
from rest_framework.response import Response
from rest_framework import serializers, status
from config.system_messages_config.error_messages import get_message
from config.system_messages_config.error_codes import ERROR_CODES

logger = logging.getLogger(__name__)


# Определение классов ошибок
class ValidationError(Exception):
    """Общая ошибка валидации."""


class FieldRequiredError(ValidationError):
    """Ошибка, возникающая при отсутствии обязательного поля."""

    def __init__(self, field_name):
        self.field_name = field_name


class FieldInvalidError(ValidationError):
    """Ошибка, возникающая при некорректном значении поля."""

    def __init__(self, field_name):
        self.field_name = field_name


class TooManyRequestsError(ValidationError):
    """Ошибка, возникающая при превышении лимита запросов."""

    def __init__(self, field_name):
        self.field_name = field_name


def handle_validation_errors(view_func):
    """
    Декоратор для обработки ошибок валидации в методах представления.

    Параметры:
    ----------
    view_func : callable
        Метод представления, который будет обернут декоратором.

    Возвращает:
    ----------
    callable
        Обернутый метод с обработкой ошибок валидации.
    """

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except serializers.ValidationError as e:
            logger.error("Validation error: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_400_BAD_REQUEST"],
                    "message": get_message("invalid_input_data"),
                    "errors": e.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except FieldRequiredError as field_error:
            logger.error("Field required error: %s", str(field_error))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_400_BAD_REQUEST"],
                    "message": get_message("field_required").format(
                        field=field_error.field_name
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except FieldInvalidError as field_error:
            logger.error("Field invalid error: %s", str(field_error))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_400_BAD_REQUEST"],
                    "message": get_message("field_invalid").format(
                        field=field_error.field_name
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except TooManyRequestsError as e:
            logger.warning("Too many requests: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_429_TOO_MANY_REQUESTS"],
                    "message": get_message("too_many_requests"),
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

    return wrapper
