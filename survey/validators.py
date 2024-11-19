import re

from django.core.validators import validate_email


def validate_telegram_nick(nick: str) -> bool:
    """
    Валидация ника в Telegram.

    Args:
        nick (str): Ник в Telegram.

    Returns:
        bool: True, если ник валиден, иначе False.
    """
    if not nick.startswith('@'):
        return False
    if len(nick) < 6 or len(nick) > 32:
        return False
    if not re.match(r'^[a-zA-Z0-9_]+$', nick[1:]):
        return False
    if '__' in nick or nick.startswith('@_') or nick.endswith('_'):
        return False
    return True


def validate_email_address(email: str) -> None:
    """
    Валидация email адреса.

    Args:
        email (str): Email адрес.

    Raises:
        ValidationError: Если email не валиден.
    """
    validate_email(email)
