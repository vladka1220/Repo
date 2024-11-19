"""
Конфигурация WSGI для Django.
"""

import os
from django.core.wsgi import get_wsgi_application

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.general_config.settings")

application = get_wsgi_application()
