FROM python:3.12-alpine AS builder
WORKDIR /app
# Копирование файла requirements.txt перед установкой зависимостей
COPY requirements.txt .
# Установка зависимостей и создание виртуального окружения
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    && apk add --no-cache libpq \
    && python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

# Этап 2: Финальная сборка образа
FROM python:3.12-alpine
WORKDIR /app
# Копирование виртуального окружения и исходного кода
COPY --from=builder /opt/venv /opt/venv
COPY . .
# Установка переменной окружения и выполнение команд
ENV PATH="/opt/venv/bin:$PATH"
RUN chmod +x /app/entrypoint.sh \
    && mkdir -p /app/logs \
    && mkdir -p /app/tmp /tmp /var/tmp /usr/tmp /tmp/gunicorn /app/logs \
    && chmod 777 /app/logs /app/tmp /tmp /var/tmp /usr/tmp /tmp/gunicorn

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]