"""
Конфигурация ASGI для Django.
"""

import os
from django.core.asgi import get_asgi_application

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.general_config.settings")

application = get_asgi_application()
