import os

import django
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Автоматически создает и применяет миграции перед запуском приложения'

    def handle(self, *args, **kwargs):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
        django.setup()
        self.stdout.write(self.style.NOTICE('Создание миграций...'))
        call_command('makemigrations')
        self.stdout.write(self.style.NOTICE('Применение миграций...'))
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Миграции успешно применены'))
