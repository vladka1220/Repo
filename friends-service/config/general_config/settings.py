"""
Настройки Django для вашего проекта.

Этот файл содержит все настройки вашего Django проекта. Включает конфигурацию
для:
- Безопасности;
- Баз данных;
- Middleware;
- Установленных приложений;
- Статических и медиафайлов;
- Логирования.

Настройки загружаются из переменных окружения, которые должны быть указаны в
файле `.env`
расположенном в корневом каталоге проекта.

Для получения дополнительной информации о доступных настройках, смотрите:
https://docs.djangoproject.com/en/stable/ref/settings/

"""

import os
from pathlib import Path
import environ
from django.utils.translation import gettext_lazy as _

# Чтение из .env файла
env = environ.Env()
environ.Env.read_env()

# Основные настройки проекта
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = env("DJANGO_SECRET_KEY")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS").split(",")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(",")
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Настройки базы данных
DATABASES = {
    "default": {
        "ENGINE": env("DJANGO_DB_ENGINE") or "django.db.backends.postgresql",
        "NAME": env("DJANGO_DB_NAME"),
        "USER": env("DJANGO_DB_USER"),
        "PASSWORD": env("DJANGO_DB_PASSWORD"),
        "HOST": env("DJANGO_DB_HOST") or "localhost",
        "PORT": env("DJANGO_DB_PORT") or "5432",
    }
}
# SQLite
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# Настройки для MongoDB
MONGO_DB_SETTINGS = {
    "NAME": env("MONGO_DB_NAME"),
    "HOST": env("MONGO_DB_HOST") or "localhost",
    "PORT": env.int("MONGO_DB_PORT") or 27017,
}

# Настройки для http запросов в сервис Profile
PROFILE_MICROSERVICE_URL = env("PROFILE_MICROSERVICE_URL")
PROFILE_USERS_BY_LIST_IDS = env("PROFILE_USERS_BY_LIST_IDS")
PROFILE_USER_CHECK = env("PROFILE_USER_CHECK")
PROFILE_USERS_SEARCH = env("PROFILE_USERS_SEARCH")

# Настройки приложений
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
    "services.service_friends",  # Добавление сервиса друзей
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
    "DEFAULT_PAGINATION_CLASS": "services.service_friends.pagination.CustomPagination",
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
    "django_keycloak.auth.backends.KeycloakAuthorizationCodeBackend",
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
    "ACCESS_TOKEN_EXPIRE_SECONDS": 36000,  # Время жизни access token
    "REFRESH_TOKEN_EXPIRE_SECONDS": 1209600,  # Время жизни refresh token
    "SCOPES": {"read": "Read scope", "write": "Write scope", "groups": "Access groups"},
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
# 

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

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

# Настройка кастомных моделей пользователя
# AUTH_USER_MODEL = "service_register.CustomUser"

# Настройка кэша
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "django_keycloak_auth",
        "TIMEOUT": KEYCLOAK_CONFIG["KEYCLOAK_CACHE_TTL"],
        "KEY_PREFIX": "django_keycloak_auth_",
    }
}
CACHE_MIDDLEWARE_KEY_PREFIX = "django_keycloak_auth_"
