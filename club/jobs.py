from datetime import timedelta

from django.utils import timezone

from .models import DailyReminder, FeedbackMessage

MESSAGE_TTL_DAYS = 30


def run_scheduled_jobs(today=None):
    """Ежедневная работа планировщика: напоминание и очистка старых заявок."""
    today = today or timezone.localdate()
    unread = FeedbackMessage.objects.filter(is_read=False).count()
    if unread:
        text = (
            f'Напоминание на {today:%d.%m.%Y}: '
            f'непрочитанных заявок на ТО — {unread}.'
        )
    else:
        text = f'{today:%d.%m.%Y}: непрочитанных заявок нет.'
    reminder, _created = DailyReminder.objects.update_or_create(
        day=today,
        defaults={'text': text},
    )
    cutoff = timezone.now() - timedelta(days=MESSAGE_TTL_DAYS)
    deleted, _details = FeedbackMessage.objects.filter(
        is_read=True,
        created_at__lt=cutoff,
    ).delete()
    return reminder, deleted
