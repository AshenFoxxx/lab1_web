import atexit
import logging
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.db import close_old_connections

logger = logging.getLogger(__name__)

_scheduler = None


def scheduled_entry():
    close_old_connections()
    try:
        from .jobs import run_scheduled_jobs
        reminder, deleted = run_scheduled_jobs()
        logger.info('%s Удалено устаревших заявок: %s', reminder.text, deleted)
    finally:
        close_old_connections()


def start_scheduler():
    """Каждый день в 09:00 по Москве запускает напоминание и очистку."""
    global _scheduler
    if _scheduler is not None:
        return _scheduler

    timezone = ZoneInfo(settings.TIME_ZONE)
    scheduler = BackgroundScheduler(timezone=timezone)
    scheduler.add_job(
        scheduled_entry,
        CronTrigger(hour=9, minute=0, timezone=timezone),
        id='daily_workshop_reminder',
        replace_existing=True,
        max_instances=1,
    )
    scheduler.start()
    _scheduler = scheduler
    atexit.register(stop_scheduler)
    logger.info('Планировщик запущен: каждый день в 09:00 (%s)', settings.TIME_ZONE)
    print(
        f'Планировщик запущен: каждый день в 09:00 ({settings.TIME_ZONE})',
        flush=True,
    )
    return scheduler


def stop_scheduler():
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None
