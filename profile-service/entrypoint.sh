#!/bin/sh
set -e

# Выполнение дополнительной команды
/opt/venv/bin/python manage.py combined_command
# Установка временного каталога
# Запуск Gunicorn с записью логов
exec gunicorn --bind 0.0.0.0:8000 \
    --workers 3 \
    profile_service.wsgi:application