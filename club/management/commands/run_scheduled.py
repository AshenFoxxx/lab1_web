from django.core.management.base import BaseCommand

from club.jobs import run_scheduled_jobs


class Command(BaseCommand):
    help = 'Один раз выполняет ежедневную задачу планировщика'

    def handle(self, *args, **options):
        reminder, deleted = run_scheduled_jobs()
        self.stdout.write(self.style.SUCCESS(reminder.text))
        self.stdout.write(f'Удалено прочитанных заявок старше 30 дней: {deleted}')
