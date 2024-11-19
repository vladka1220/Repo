"""
Модуль для работы с сообщениями и их локализацией.

Содержит словарь сообщений для различных состояний регистрации и аутентификации
в двух языках: английском и русском. Также включает функцию для получения
сообщения по ключу с учетом текущего языка.

Словарь сообщений:
- registration_successful: Успешная регистрация
- user_creation_error: Ошибка при создании пользователя
- invalid_input_data: Некорректные входные данные
- invalid_credentials: Некорректные учетные данные
- auth_server_error: Ошибка на сервере аутентификации
- password_mismatch: Несоответствие паролей
- email_already_registered: Email уже зарегистрирован
- email_required: Требуется email
- email_invalid: Некорректный адрес email
- password_required: Требуется пароль
- password_min_length: Минимальная длина пароля - 8 символов
- password_max_length: Максимальная длина пароля - 128 символов
- registration_confirmation_subject: Подтверждение регистрации
- registration_confirmation_message: Сообщение о подтверждении регистрации
- email_sending_error: Ошибка при отправке письма
- subject_not_found_log: Не найдена тема для письма
- current_language_log: Текущий язык
- message_not_found_log: Не найдено сообщение для письма
- no_email_provided_log: У юзера нет почты
- sending_confirmation_email_log: Письмо о подтверждении отправляется
- confirmation_email_sent_log: Письмо о подтверждении отправлено
- registration_confirmation_link_path: Путь для подтверждения регистрации
"""

import logging
from django.utils.translation import get_language

logger = logging.getLogger(__name__)

MESSAGES = {
    "registration_successful": {
        "en": "Registration completed successfully! Check your email for account confirmation.",
        "ru": "Регистрация успешна! Проверьте вашу почту для подтверждения.",
    },
    "user_creation_error": {
        "en": "An error occurred while creating the user: {error}",
        "ru": "Произошла ошибка при создании пользователя: {error}",
    },
    "invalid_input_data": {
        "en": "Invalid input data.",
        "ru": "Некорректные входные данные.",
    },
    "invalid_credentials": {
        "en": "Invalid credentials provided.",
        "ru": "Предоставлены некорректные учетные данные.",
    },
    "auth_server_error": {
        "en": "An error occurred on the authentication server.",
        "ru": "Произошла ошибка на сервере аутентификации.",
    },
    "password_mismatch": {
        "en": "Passwords do not match.",
        "ru": "Пароли не совпадают.",
    },
    "email_already_registered": {
        "en": "This email is already registered.",
        "ru": "Этот email уже зарегистрирован.",
    },
    "email_required": {
        "en": "Email is required.",
        "ru": "Требуется email.",
    },
    "email_invalid": {
        "en": "Invalid email address.",
        "ru": "Некорректный адрес email.",
    },
    "password_required": {
        "en": "Password is required.",
        "ru": "Требуется пароль.",
    },
    "password_min_length": {
        "en": "Password must be at least 8 characters long.",
        "ru": "Пароль должен быть не менее 8 символов.",
    },
    "password_max_length": {
        "en": "Password cannot exceed 128 characters.",
        "ru": "Пароль не может превышать 128 символов.",
    },
    "registration_confirmation_subject": {
        "en": "Registration Confirmation",
        "ru": "Подтверждение регистрации",
    },
    "registration_confirmation_message": {
        "en": "Dear {first_name}, thank you for registering! Please confirm your email by clicking the link: {confirmation_link}",
        "ru": "Уважаемый {first_name}, спасибо за регистрацию! Пожалуйста, подтвердите ваш email, пройдя по ссылке: {confirmation_link}",
    },
    "email_sending_error": {
        "en": "An error occurred while sending the email: {error}",
        "ru": "Произошла ошибка при отправке письма: {error}",
    },
    "subject_not_found_log": {
        "en": "Subject not found for key: {key}",
        "ru": "Тема не найдена для ключа: {key}",
    },
    "current_language_log": {
        "en": "Current language: {language}",
        "ru": "Текущий язык: {language}",
    },
    "message_not_found_log": {
        "en": "Message not found for key: {key}",
        "ru": "Сообщение не найдено для ключа: {key}",
    },
    "no_email_provided_log": {
        "en": "No email provided for user: {username}",
        "ru": "Не предоставлен email для пользователя: {username}",
    },
    "sending_confirmation_email_log": {
        "en": "Sending confirmation email to {to_email} with subject '{subject}'",
        "ru": "Отправка письма с подтверждением на {to_email} с темой '{subject}'",
    },
    "confirmation_email_sent_log": {
        "en": "Confirmation email sent to: {to_email}",
        "ru": "Письмо с подтверждением отправлено на: {to_email}",
    },
    "registration_confirmation_link_path": {
        "en": "Auth",
        "ru": "Auth",
    },
    "account_locked": {
        "en": "Your account is locked.",
        "ru": "Ваша учетная запись заблокирована.",
    },
    "account_inactive": {
        "en": "Your account is inactive.",
        "ru": "Ваша учетная запись неактивна.",
    },
    "unexpected_error": {
        "en": "An unexpected error occurred. Please try again later.",
        "ru": "Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже.",
    },
    "too_many_requests": {
        "en": "Too many requests. Please try again later.",
        "ru": "Слишком много запросов. Пожалуйста, попробуйте позже.",
    },
}


def get_message(key: str) -> str:
    """
    Получает сообщение по ключу и языку.

    :param key: Ключ сообщения
    :return: Сообщение в указанном языке или ключ, если сообщение не найдено
    """
    # Получаем текущий язык или используем язык по умолчанию
    language_code = get_language()[:2] if get_language() else "en"

    # Получаем словарь сообщений для указанного ключа
    message_dict = MESSAGES.get(key)

    if message_dict is None:  # Если ключа нет в словаре
        return key  # Возвращаем ключ, если сообщения не найдено

    # Логируем информацию о ключах
    logger.debug("Getting message for key: %s", key)
    logger.debug("Available keys for current language: %s", message_dict.keys())

    # Возвращаем сообщение на текущем языке или на английском, если текущий язык не найден
    return message_dict.get(language_code, message_dict.get("en", key))
