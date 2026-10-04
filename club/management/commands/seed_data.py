from django.core.management.base import BaseCommand

from club.seed import refresh_demo_content


class Command(BaseCommand):
    help = 'Заполняет или обновляет демо-данные мастерской'

    def handle(self, *args, **options):
        refresh_demo_content()
        self.stdout.write(self.style.SUCCESS('Демо-данные мастерской готовы.'))
