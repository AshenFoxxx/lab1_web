from django.apps import AppConfig
from django.db.models.signals import post_migrate


def _seed(sender, **kwargs):
    from django.db import connection
    from .seed import seed_if_empty

    tables = connection.introspection.table_names()
    if 'club_page' in tables:
        seed_if_empty()


class ClubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'club'
    verbose_name = 'Мастерская Маяк'

    def ready(self):
        post_migrate.connect(_seed, sender=self, dispatch_uid='club_seed')
