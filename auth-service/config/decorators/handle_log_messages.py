"""
Модуль для логирования и обработки исключений в представлениях.

Этот модуль содержит декоратор `log_messages`, который объединяет
логирование входящих данных, отсутствия email и обработку исключений, связанных с
валидацией и другими ошибками.

Импортированные библиотеки:
- functools: для использования функции wraps.
- rest_framework.response: для работы с ответами API.
- rest_framework.status: для использования статусов HTTP.
- rest_framework.exceptions: для обработки исключений валидации.
- logging: для ведения журнала событий.
"""

import logging
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from config.system_messages_config.error_messages import get_message

logger = logging.getLogger(__name__)


def log_messages(view_func):
    """
    Декоратор для логирования входящих данных, отсутствия email и обработки исключений.

    Параметры:
    ----------
    view_func : Callable
        Метод, который будет обернут декоратором.

    Возвращает:
    ----------
    Callable
        Обернутый метод с логированием и обработкой исключений.
    """

    @wraps(view_func)
    def wrapper(self, *args, **kwargs):
        # Логгируем отсутствие email
        user_email = kwargs.get("email")
        if not user_email:
            logger.warning(
                get_message("no_email_provided_log").format(
                    username=kwargs.get("username", "Unknown User")
                )
            )

        logger.info(
            get_message("sending_confirmation_email_log").format(
                to_email=user_email,
                subject=get_message("registration_confirmation_subject"),
            )
        )

        # Логгируем входящие данные
        logger.info(
            "Method: %s, Args: %s, Kwargs: %s", view_func.__name__, args, kwargs
        )

        try:
            # Вызов оригинального представления
            response = view_func(self, *args, **kwargs)

            # Логируем успешное выполнение метода и ответ
            logger.info("Successfully executed method: %s", view_func.__name__)
            logger.info(
                "Response: %s",
                response.data if isinstance(response, Response) else response,
            )

            # Логгируем отправку письма (если есть успешный статус)
            if (
                isinstance(response, Response)
                and response.status_code == status.HTTP_201_CREATED
            ):
                logger.info(
                    get_message("confirmation_email_sent_log").format(
                        to_email=user_email
                    )
                )

            return response

        except DRFValidationError as e:
            logger.error("Validation error in %s: %s", view_func.__name__, str(e))
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Validation error.",
                    "errors": e.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except (ValueError, TypeError) as e:
            logger.exception("Critical error in %s: %s", view_func.__name__, str(e))
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "An unexpected error occurred.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapper
