import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
DB_ENGINE = os.environ.get("DB_ENGINE")
DB_NAME = os.environ.get("DB_NAME")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DEBUG = os.environ.get("DEBUG")
#STATIC_URL = os.environ.get("STATIC_URL")
#STATIC_ROOT = os.environ.get("STATIC_ROOT")
#STATICFILES_DIRS = os.environ.get("STATICFILES_DIRS")
# Загружаем ALLOWED_HOSTS как список строк
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
