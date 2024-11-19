import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает пользователя test, если он отсутствует'

    def handle(self, *args, **kwargs):
        load_dotenv()
        username = 'test'
        password = 'test'
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(f'Пользователь {username} создан'))
        else:
            self.stdout.write(self.style.WARNING(f'Пользователь {username} уже существует'))
