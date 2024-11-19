# Этап 1: Сборка зависимостей и подготовка приложения
FROM python:3.12.5-slim AS build

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости, необходимые для сборки Python пакетов
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем виртуальное окружение для Python
RUN python -m venv /opt/venv

# Копируем файл с зависимостями
COPY requirements.txt ./

# Устанавливаем Python зависимости в виртуальное окружение
RUN /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Копируем все файлы приложения
COPY . .

# Этап 2: Финальная сборка
FROM python:3.12.5-slim AS production

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем приложение из этапа сборки
COPY --from=build /app /app

# Копируем виртуальное окружение
COPY --from=build /opt/venv /opt/venv

# Добавляем виртуальное окружение в PATH
ENV PATH="/opt/venv/bin:$PATH"

# Выполняем команды настройки
RUN python manage.py collectstatic --noinput \
    && chmod +x /app/entrypoint.sh \
    && mkdir -p /app/logs /app/tmp /tmp /var/tmp /usr/tmp /tmp/gunicorn \
    && chmod 755 /app/logs /app/tmp /tmp /var/tmp /usr/tmp /tmp/gunicorn

# Открываем необходимый порт
EXPOSE 8000

# Указываем точку входа в контейнер
ENTRYPOINT ["/app/entrypoint.sh"]