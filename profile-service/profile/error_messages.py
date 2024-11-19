from django.utils.translation import get_language

# Определение сообщений об ошибках
MESSAGES = {
    "invalid_user_id": {
        "en": "Invalid user ID provided.",
        "ru": "Предоставлен некорректный ID пользователя.",
    },
    "not_found": {
        "en": "No records found.",
        "ru": "Записи не найдены.",
    },
    "forbidden": {
        "en": "You do not have permission to perform this action.",
        "ru": "У вас нет прав для выполнения данного действия.",
    },
}


def get_message(key: str, lang: str = "en") -> str:
    """
    Получает сообщение по ключу и языку.

    :param key: Ключ сообщения
    :param lang: Язык сообщения ("en" или "ru")
    :return: Сообщение на указанном языке
    """
    language_code = lang or get_language()[:2] or "en"
    message_entry = MESSAGES.get(key, {})
    return message_entry.get(language_code, message_entry.get("en", key))
