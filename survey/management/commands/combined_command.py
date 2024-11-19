from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Запускает несколько команд управления поочередно'

    def handle(self, *args, **options):
        try:
            # Запускаем проверку и обновление миграций
            call_command('auto_migrate')
            self.stdout.write(self.style.SUCCESS('Успешно выполнена команда auto_migrate'))

            # Проверяем наличие админа, создаем если нету
            call_command('check_admin')
            self.stdout.write(self.style.SUCCESS('Успешно выполнена команда check_admin'))

            # Заменяем пароль администратора на установленный в настройках
            call_command('change_admin_password')
            self.stdout.write(self.style.SUCCESS('Успешно выполнена команда check_admin'))

        except CommandError as e:
            self.stderr.write(self.style.ERROR(f'Ошибка: {e}'))
