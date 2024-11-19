#!/bin/sh
set -e

# Применение миграций
/opt/venv/bin/python manage.py migrate --noinput
# Выполнение дополнительной команды
/opt/venv/bin/python manage.py combined_command
# Установка временного каталога
# Запуск Gunicorn с записью логов
exec gunicorn --bind 0.0.0.0:8000 \
    --workers 3 \
    config.general_config.wsgi:application
