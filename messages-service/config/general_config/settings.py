"""
Настройки проекта Django для messages_service.
"""

import os
from pathlib import Path
import environ
import mongoengine
from django.utils.translation import gettext_lazy as _

# Чтение переменных из .env файла
env = environ.Env()
environ.Env.read_env()

# Основные настройки проекта
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = env("DJANGO_SECRET_KEY")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS")
DEBUG = env("DEBUG") != "false"
ALLOWED_HOSTS = [env("DJANGO_ALLOWED_HOSTS") or "0.0.0.0"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Настройки базы данных PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": env("DJANGO_DB_ENGINE")
        or "django.db.backends.postgresql",  # Драйвер базы данных
        "NAME": env("DJANGO_DB_NAME"),  # Имя базы данных
        "USER": env("DJANGO_DB_USER"),  # Пользователь базы данных
        "PASSWORD": env("DJANGO_DB_PASSWORD"),  # Пароль пользователя
        "HOST": env("DJANGO_DB_HOST") or "localhost",  # Хост базы данных
        "PORT": env("DJANGO_DB_PORT") or "5432",  # Порт базы данных
    }
}

# Настройки базы данных MongoDB с использованием MongoEngine
mongoengine.connect(
    db=env("MONGO_DB_NAME"),  # Драйвер базы данных
    host=env("MONGO_HOST"),  # Хост базы данных
    port=env.int("MONGO_PORT"),  # Порт базы данных
    username=env("MONGO_USERNAME"),  # Пользователь базы данных
    password=env("MONGO_PASSWORD"),  # Пароль пользователя
    authentication_source=env("MONGO_AUTH_SOURCE"),  # Источник аутентификации
)

# Установленные приложения
INSTALLED_APPS = [
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "oauth2_provider",
    "oauthlib",
    "django_keycloak",
    "django_keycloak_auth",
    "services.messages_service",  # Наш сервис сообщений
]

# Мидлвары
MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Расширение WhiteNoise для статик файлов
    "django.middleware.security.SecurityMiddleware",  # Защита от уязвимостей безопасности
    "django.contrib.sessions.middleware.SessionMiddleware",  # Обработка сессий пользователей
    "django.middleware.common.CommonMiddleware",  # Добавление общих заголовков
    "django.middleware.csrf.CsrfViewMiddleware",  # Защита от CSRF атак
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Аутентификация пользователей
    "django.contrib.messages.middleware.MessageMiddleware",  # Обработка сообщений между запросами
    "django.middleware.locale.LocaleMiddleware",  # Обработка языковых предпочтений
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Защита от clickjacking
    "django_keycloak_auth.middleware.KeycloakMiddleware",  # Интеграция с Keycloak
]

# Настройки Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

# Настройки WSGI и ASGI приложений
WSGI_APPLICATION = "django_keycloak_auth.wsgi.application"
ASGI_APPLICATION = "django_keycloak_auth.asgi.application"

# Настройки для Keycloak
AUTHENTICATION_BACKENDS = (
    "django_keycloak_auth.backends.KeycloakBackend",
    "django.contrib.auth.backends.ModelBackend",
)

# Параметры для подключения к Keycloak
KEYCLOAK_CONFIG = {
    "KEYCLOAK_SERVER_URL": env("KEYCLOAK_SERVER_URL"),
    "KEYCLOAK_REALM": env("KEYCLOAK_REALM"),
    "KEYCLOAK_CLIENT_ID": env("KEYCLOAK_CLIENT_ID"),
    "KEYCLOAK_CLIENT_SECRET_KEY": env("KEYCLOAK_CLIENT_SECRET_KEY"),
    "KEYCLOAK_CACHE_TTL": env("KEYCLOAK_CACHE_TTL"),
    "LOCAL_DECODE": env.bool("LOCAL_DECODE"),
}
KEYCLOAK_EXEMPT_URIS = []

# Настройки для OAuth2.0
OAUTH2_PROVIDER = {
    "OAUTH2_BACKEND_CLASS": "oauth2_provider.oauth2_backends.OAuthLibCore",
    "ACCESS_TOKEN_EXPIRE_SECONDS": env.int("OAUTH2_ACCESS_TOKEN_EXPIRE_SECONDS")
    or 36000,
    "REFRESH_TOKEN_EXPIRE_SECONDS": env.int("OAUTH2_REFRESH_TOKEN_EXPIRE_SECONDS")
    or 1209600,
    "SCOPES": {
        "read": env("OAUTH2_SCOPE_READ") or "Read scope",
        "write": env("OAUTH2_SCOPE_WRITE") or "Write scope",
        "groups": env("OAUTH2_SCOPE_GROUPS") or "Access groups",
    },
    "MODELS": {
        "ACCESS_TOKEN": env("OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL")
        or "oauth2_provider.AccessToken",
        "APPLICATION": env("OAUTH2_PROVIDER_APPLICATION_MODEL")
        or "oauth2_provider.Application",
        "ID_TOKEN": env("OAUTH2_PROVIDER_ID_TOKEN_MODEL") or "oauth2_provider.IDToken",
        "GRANT": env("OAUTH2_PROVIDER_GRANT_MODEL") or "oauth2_provider.Grant",
        "REFRESH_TOKEN": env("OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL")
        or "oauth2_provider.RefreshToken",
    },
}

# Валидаторы для пароля
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Настройка статических файлов
STATIC_URL = env("STATIC_URL") or "/static/"
STATIC_ROOT = env("STATIC_ROOT") or os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = env.list("STATICFILES_DIRS") or [os.path.join(BASE_DIR, "static")]

# Настройки логгирования
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "graylog": {
            "level": "DEBUG",
            "class": "graypy.GELFHandler",
            "host": env("GRAYLOG_HOST"),
            "port": env.int("GRAYLOG_PORT") or 12201,
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["graylog", "console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# Настройки безопасности
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_POLICY = "same-origin"
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

# Интернационализация
LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
]
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# Настройки пути URL
ROOT_URLCONF = "config.general_config.urls"

# Настройка кэша
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "django_keycloak_auth",
        "TIMEOUT": KEYCLOAK_CONFIG["KEYCLOAK_CACHE_TTL"],
        "KEY_PREFIX": "django_keycloak_auth_",
    }
}
