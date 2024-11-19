from django.utils.translation import get_language

# Определение сообщений об ошибках
MESSAGES = {
    "friend_request_sent": {
        "en": "Friend request sent successfully.",
        "ru": "Запрос на добавление в друзья успешно отправлен.",
    },
    "friend_request_already_sent": {
        "en": "Friend request has already been sent.",
        "ru": "Запрос на добавление в друзья уже отправлен.",
    },
    "friend_request_not_found": {
        "en": "Friend request not found.",
        "ru": "Запрос на добавление в друзья не найден.",
    },
    "friend_added": {
        "en": "Friend added successfully.",
        "ru": "Друг успешно добавлен.",
    },
    "friend_already_added": {
        "en": "This user is already your friend.",
        "ru": "Этот пользователь уже в друзьях.",
    },
    "favorite_added": {
        "en": "User added to favorites.",
        "ru": "Пользователь добавлен в избранное.",
    },
    "favorite_already_added": {
        "en": "This user is already in your favorites.",
        "ru": "Этот пользователь уже в избранном.",
    },
    "invalid_user_id": {
        "en": "Invalid user ID provided.",
        "ru": "Предоставлен некорректный ID пользователя.",
    },
    "not_found": {
        "en": "No records found.",
        "ru": "Записи не найдены.",
    },
    "already_friends": {
        "en": "You are already friends with this user.",
        "ru": "Вы уже в друзьях с этим пользователем.",
    },
    "cannot_send_request_to_self": {
        "en": "You cannot send a friend request to yourself.",
        "ru": "Вы не можете отправить запрос в друзья самому себе.",
    },
    "friend_not_found": {
        "en": "Friend not found.",
        "ru": "Друг не найден.",
    },
    "favorite_not_found": {
        "en": "Favorite user not found.",
        "ru": "Пользователь в избранном не найден.",
    },
    "friend_deleted": {
        "en": "Friend deleted successfully.",
        "ru": "Друг успешно удален.",
    },
    "favorite_deleted": {
        "en": "User removed from favorites.",
        "ru": "Пользователь удален из избранного.",
    },
    "error_processing_request": {
        "en": "An error occurred while processing the request: {error}",
        "ru": "Произошла ошибка при обработке запроса: {error}",
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
