"""
Модуль содержит декоратор для обработки серверных ошибок.

Декоратор `handle_server_errors` обрабатывает различные типы
исключений, возникающих при работе с сервером, и возвращает соответствующие
ответы с ошибками.
"""

import logging
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from config.system_messages_config.error_messages import get_message
from config.system_messages_config.error_codes import ERROR_CODES

logger = logging.getLogger(__name__)


class ServerError(Exception):
    """Общая ошибка сервера."""


class AuthServerError(ServerError):
    """Ошибка, возникающая при аутентификации на сервере."""


class UnexpectedError(ServerError):
    """Ошибка, возникающая при неожиданном сбое на сервере."""


class EmailSendingError(ServerError):
    """Ошибка, возникающая при отправке электронной почты."""


class InternalServerError(ServerError):
    """Ошибка, возникающая при внутреннем сбое сервера."""


def handle_server_errors(view_func):
    """
    Декоратор для обработки серверных ошибок в методах представления.

    Параметры:
    ----------
    view_func : callable
        Метод представления, который будет обернут декоратором.

    Возвращает:
    ----------
    callable
        Обернутый метод с обработкой ошибок сервера.
    """

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except AuthServerError as e:
            logger.error("Authentication server error: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_500_INTERNAL_SERVER_ERROR"],
                    "message": get_message("auth_server_error"),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except UnexpectedError as e:
            logger.error("Unexpected error: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_500_INTERNAL_SERVER_ERROR"],
                    "message": get_message("unexpected_error"),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except EmailSendingError as e:
            logger.error("Email sending error: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_500_INTERNAL_SERVER_ERROR"],
                    "message": get_message("email_sending_error").format(error=str(e)),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except InternalServerError as e:
            logger.error("Internal server error: %s", str(e))
            return Response(
                {
                    "status": ERROR_CODES["HTTP_500_INTERNAL_SERVER_ERROR"],
                    "message": get_message("internal_server_error"),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapper
