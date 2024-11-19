import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        username = 'admin'

        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Password for user "{username}" has been successfully changed.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist.'))
