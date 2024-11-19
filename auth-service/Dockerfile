# Этап 1: Сборка зависимостей и подготовка приложения
FROM python:3.12.5-slim AS build
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
COPY requirements.txt .
RUN /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
COPY . .

# Этап 2: Финальная сборка
FROM python:3.12.5-slim AS production
WORKDIR /app
# Копируем приложение и виртуальное окружение из этапа сборки
COPY --from=build /app /app
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN /opt/venv/bin/python manage.py collectstatic --noinput \
    && chmod +x /app/entrypoint.sh \
    && mkdir -p /app/logs /app/tmp /tmp /var/tmp /usr/tmp /tmp/gunicorn \
    && chmod 755 /app/logs /app/tmp /tmp /var/tmp /usr/tmp /tmp/gunicorn
EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
