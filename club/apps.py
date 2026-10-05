import os
import sys

from django.apps import AppConfig
from django.db.models.signals import post_delete, post_migrate, post_save


def _seed(sender, **kwargs):
    from django.db import connection
    from .seed import seed_if_empty

    tables = connection.introspection.table_names()
    if 'club_page' in tables:
        seed_if_empty()


def _invalidate_cache(sender, **kwargs):
    from .caching import invalidate_public_cache
    invalidate_public_cache()


class ClubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'club'
    verbose_name = 'Мастерская Маяк'

    def ready(self):
        post_migrate.connect(_seed, sender=self, dispatch_uid='club_seed')
        from .models import GalleryImage, Page
        for model in (Page, GalleryImage):
            post_save.connect(
                _invalidate_cache,
                sender=model,
                dispatch_uid=f'club_cache_{model.__name__}',
            )
            post_delete.connect(
                _invalidate_cache,
                sender=model,
                dispatch_uid=f'club_cache_del_{model.__name__}',
            )
        # С автоперезагрузкой планировщик стартует только в дочернем процессе.
        runserver = 'runserver' in sys.argv
        child = os.environ.get('RUN_MAIN') == 'true' or '--noreload' in sys.argv
        if runserver and child:
            from .scheduler import start_scheduler
            start_scheduler()
