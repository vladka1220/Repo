"""
Настройки Django для вашего проекта.

Этот файл содержит все настройки вашего Django проекта.
Включает конфигурацию для:
- Безопасности;
- Баз данных;
- Middleware;
- Установленных приложений;
- Статических и медиафайлов;
- Логирования.

Настройки загружаются из переменных окружения.

Для получения дополнительной информации о доступных настройках, смотрите:
https://docs.djangoproject.com/en/stable/ref/settings/
"""

from pathlib import Path
import os
import environ
from django.utils.translation import gettext_lazy as _

env = environ.Env()
environ.Env.read_env()

# Основные настройки проекта
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Настройки CSRF_TRUSTED_ORIGINS
CSRF_TRUSTED_ORIGINS = []
csrf_origins = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")

for origin in csrf_origins:
    origin = origin.strip()
    if origin:
        if "://" in origin:  # Если схема уже присутствует
            CSRF_TRUSTED_ORIGINS.append(origin)
        elif (
                origin.replace(".", "").isdigit()
                or "/" in origin
                or "*" in origin
                or origin == "localhost"
        ):
            # Для IP-адресов, подсетей, шаблонов со звездочкой и localhost
            CSRF_TRUSTED_ORIGINS.append(f"http://{origin}")
            CSRF_TRUSTED_ORIGINS.append(f"https://{origin}")
        else:
            # Для доменных имен добавляем только HTTPS
            CSRF_TRUSTED_ORIGINS.append(f"https://{origin}")

# Настройки CORS
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]
CORS_ALLOW_METHODS = [
    method.strip()
    for method in os.environ.get("CORS_ALLOW_METHODS", "").split(",")
    if method.strip()
]
CORS_ALLOW_HEADERS = [
    header.strip()
    for header in os.environ.get("CORS_ALLOW_HEADERS", "").split(",")
    if header.strip()
]
CORS_ALLOW_CREDENTIALS = (
        os.environ.get("CORS_ALLOW_CREDENTIALS", "True").lower() == "true"
)

# Фильтрация пустых строк
CORS_ALLOWED_ORIGINS = list(filter(None, CORS_ALLOWED_ORIGINS))

# Настройки базы данных PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DJANGO_DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("DJANGO_DB_NAME"),
        "USER": os.environ.get("DJANGO_DB_USER"),
        "PASSWORD": os.environ.get("DJANGO_DB_PASSWORD"),
        "HOST": os.environ.get("DJANGO_DB_HOST"),
        "PORT": os.environ.get("DJANGO_DB_PORT"),
    }
}

# Настройки приложений
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "minio_storage",
    "rest_framework",
    "drf_spectacular",

    "profile.apps.ProfileConfig",
]

# Мидлвары
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Настройки WSGI приложения
WSGI_APPLICATION = "profile_service.wsgi.application"

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

# Настройки логирования
# LOG_DIR = os.path.join(BASE_DIR, "logs")
# if LOG_DIR and not os.path.exists(LOG_DIR):
#    os.makedirs(LOG_DIR)
# log_filename = "error.log"
# log_file_path = os.path.join(LOG_DIR, log_filename)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'profile_service': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Настройки шаблонов
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Настройки пользователя
AUTH_USER_MODEL = 'profile.User'

# Настройки безопасности
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

# Интернационализация
LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
]
LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "en-us")
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# Настройки статических и медиафайлов
STATIC_URL = "/static/"
MEDIA_URL = ""

# Настройки хранения файлов
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Установите URL для аватарки по умолчанию
DEFAULT_AVATAR_URL = "https://t4.ftcdn.net/jpg/08/01/47/93/360_F_801479395_lZeVjLIbUhVKS2WyYu2AqMnEBhHpv6gJ.jpg"

# Настройки Minio
# DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"
# STATICFILES_STORAGE = "minio_storage.storage.MinioStaticStorage"

# MINIO_STORAGE_ENDPOINT = 'minio-0.minio.minio-storage.svc.cluster.local:9000'
# MINIO_STORAGE_ACCESS_KEY = 'JoJoMarletto'
# MINIO_STORAGE_SECRET_KEY = 'mxgwQiLZz4ELkjdwAcCJsefMz5quCmpcdjdNsCj7UXTPn2kuiq'
# MINIO_STORAGE_USE_HTTPS = False  # Установить True, если используется HTTPS
#
# # Укажите название bucket
# MINIO_STORAGE_MEDIA_BUCKET_NAME = 'local-media'
# MINIO_STORAGE_STATIC_BUCKET_NAME = 'local-static'
#
# MINIO_STORAGE_MEDIA_URL = f'http://{"minio-0.minio.minio-storage.svc.cluster.local:9000" or "localhost:9000"}/local-media'
# MINIO_STORAGE_STATIC_URL = f'http://{"minio-0.minio.minio-storage.svc.cluster.local:9000" or "localhost:9000"}/local-static'
#
# # Дополнительные настройки
# MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
# MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True

# Настройки пути URL
ROOT_URLCONF = "profile_service.urls"

SPECTACULAR_SETTINGS = {
    'TITLE': 'Profile Service',
    'DESCRIPTION': 'Swagger Profile Service',
    'VERSION': '0.0.8',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        "filter": True,  # поиск по тегам
    },
}
