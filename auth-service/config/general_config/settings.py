"""
Настройки Django для вашего проекта.

Этот файл содержит все основные настройки вашего Django проекта.
Он включает в себя конфигурацию для:

- Безопасности: Настройки безопасности, такие как CSRF и CORS.
- Базы данных: Конфигурация для подключения к PostgreSQL.
- Middleware: Настройки промежуточного ПО для обработки запросов.
- Установленные приложения: Список приложений, которые используются в проекте.
- Статических и медиафайлов: Настройки для обслуживания статических файлов.
- Интернационализации: Поддержка различных языков и временных зон.
- Логирования: Настройка системы логирования для отслеживания событий.
- ОAUTH2.0: Настройки для аутентификации и авторизации через OAUTH2.

Настройки загружаются из переменных окружения для обеспечения
безопасности и конфиденциальности.

Дополнительная информация о доступных настройках:
https://docs.djangoproject.com/en/stable/ref/settings/

"""

####################
# CORE             #
####################

from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _

print(os.environ.get("DJANGO_DB_ENGINE"))

# Основные настройки проекта
DEBUG = True
PYTHONPATH = os.environ.get("PYTHONPATH")
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")
DEFAULT_SCHEME = os.environ.get("DEFAULT_SCHEME")

# Интернационализация
LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "ru")
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
]

# Настройки почтового сервиса
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
EMAIL_SITE_DOMAIN = os.environ.get("EMAIL_SITE_DOMAIN")

# Настройки коннектов между сервисами
PROFILE_SERVICE_URL = os.environ.get("PROFILE_SERVICE_URL")

# Настройки базы данных PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DJANGO_DB_ENGINE"),
        "NAME": os.environ.get("DJANGO_DB_NAME"),
        "USER": os.environ.get("DJANGO_DB_USER"),
        "PASSWORD": os.environ.get("DJANGO_DB_PASSWORD"),
        "HOST": os.environ.get("DJANGO_DB_HOST"),
        "PORT": os.environ.get("DJANGO_DB_PORT"),
    }
}

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
    "corsheaders",
    "services.service_register",
    "services.service_auth",
    "services.service_pass_reminder.reset_pass",
    "services.service_pass_reminder.confirm_pass",
]

# Настройки темплейтов
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

# Настройка поля по умолчанию для автоинкрементных идентификаторов
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URL конфигурация
ROOT_URLCONF = "config.general_config.urls"

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

##############
# MIDDLEWARE #
##############

# Мидлвары
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # CORS middleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

############
# SESSIONS #
############

# Настройки сессий проводим через Keycloak

##################
# AUTHENTICATION #
##################

# Настройка кастомных моделей пользователя
AUTH_USER_MODEL = "service_register.CustomUser"

# Настройки для Keycloak
AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

# Настройки хэширования для всего проекта и всех сервисов
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

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

# Параметры для подключения к Keycloak
KEYCLOAK_CONFIG = {
    "KEYCLOAK_SERVER_URL": os.environ.get("KEYCLOAK_SERVER_URL"),
    "KEYCLOAK_REALM": os.environ.get("KEYCLOAK_REALM"),
    "KEYCLOAK_CLIENT_ID": os.environ.get("KEYCLOAK_CLIENT_ID"),
    "KEYCLOAK_CLIENT_SECRET_KEY": os.environ.get("KEYCLOAK_CLIENT_SECRET_KEY"),
    "KEYCLOAK_CACHE_TTL": os.environ.get("KEYCLOAK_CACHE_TTL"),
    "KEYCLOAK_ADMIN_USERNAME": os.environ.get("KEYCLOAK_ADMIN_USERNAME"),
    "KEYCLOAK_ADMIN_PASSWORD": os.environ.get("KEYCLOAK_ADMIN_PASSWORD"),
    "KEYCLOAK_REDIRECT_URI": os.environ.get("KEYCLOAK_REDIRECT_URI"),
    "LOCAL_DECODE": os.environ.get("LOCAL_DECODE", "False").lower() == "true",
}

# Настройки для OAuth2.0
OAUTH2_BACKEND_CLASS = "oauth2_provider.oauth2_backends.OAuthLibCore"
ACCESS_TOKEN_EXPIRE_SECONDS = int(
    os.environ.get("OAUTH2_ACCESS_TOKEN_EXPIRE_SECONDS", 36000)
)
REFRESH_TOKEN_EXPIRE_SECONDS = int(
    os.environ.get("OAUTH2_REFRESH_TOKEN_EXPIRE_SECONDS", 1209600)
)
OAUTH2_SCOPE_READ = os.environ.get("OAUTH2_SCOPE_READ", "Read scope")
OAUTH2_SCOPE_WRITE = os.environ.get("OAUTH2_SCOPE_WRITE", "Write scope")
OAUTH2_SCOPE_GROUPS = os.environ.get("OAUTH2_SCOPE_GROUPS", "Access groups")
OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL = os.environ.get(
    "OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL", "oauth2_provider.AccessToken"
)
OAUTH2_PROVIDER_APPLICATION_MODEL = os.environ.get(
    "OAUTH2_PROVIDER_APPLICATION_MODEL", "oauth2_provider.Application"
)
OAUTH2_PROVIDER_ID_TOKEN_MODEL = os.environ.get(
    "OAUTH2_PROVIDER_ID_TOKEN_MODEL", "oauth2_provider.IDToken"
)
OAUTH2_PROVIDER_GRANT_MODEL = os.environ.get(
    "OAUTH2_PROVIDER_GRANT_MODEL", "oauth2_provider.Grant"
)
OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL = os.environ.get(
    "OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL", "oauth2_provider.RefreshToken"
)

###########
# SIGNING #
###########

# Класс для подписи и проверки временных данных
SIGNING_BACKEND = "django.core.signing.TimestampSigner"

########
# CSRF #
########

CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
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
            # Для IP-адресов, подсетей, шаблонов с звездочкой и localhost
            CSRF_TRUSTED_ORIGINS.append(f"http://{origin}")
            CSRF_TRUSTED_ORIGINS.append(f"https://{origin}")
        else:
            # Для доменных имен добавляем только HTTPS
            CSRF_TRUSTED_ORIGINS.append(f"https://{origin}")

############
# MESSAGES #
############

# Класс, который будет использоваться как хранилище сообщений
MESSAGE_STORAGE = "django.contrib.messages.storage.fallback.FallbackStorage"

###########
# LOGGING #
###########

# Настройки логирования
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

###########
# TESTING #
###########

# Имя класса, который будет использоваться для запуска набора тестов
# TEST_RUNNER = "django.test.runner.DiscoverRunner"

# Приложения, которые не нужно сериализовать при создании тестовой базы данных
# (только приложения с миграциями должны быть вначале)
# TEST_NON_SERIALIZED_APPS = []

############
# FIXTURES #
############

# Список директорий для поиска фикстур

###############
# STATICFILES #
###############

# Использование whitenoise для обслуживания статических файлов
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

##############
# MIGRATIONS #
##############

# Переопределения модулей миграции для приложений по метке приложения.
# Записать здесь все возможные переопределения работы стандартных миграций.

#################
# SYSTEM CHECKS #
#################

# Список всех проблем, сгенерированных системными проверками, которые следует подавить.
# Легкие проблемы, такие как предупреждения, информация или отладка, не будут генерировать сообщение.
# Подавление серьезных проблем, таких как ошибки и критические ошибки, не приводит к скрытию сообщения,
# но Django не будет останавливать вас, например, от запуска сервера.

#######################
# SECURITY MIDDLEWARE #
#######################

# Настройки безопасности
SESSION_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_HTTPONLY = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_POLICY = "same-origin"
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

#########
# CACHE #
#########

# Здесь будут настройки кэша
