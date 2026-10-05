from datetime import timedelta

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.utils import timezone

from club.caching import benchmark_home, get_menu_pages, get_public_catalog
from club.jobs import run_scheduled_jobs
from club.models import DailyReminder, FeedbackMessage, Page


class SmokeTests(TestCase):
    def test_public_pages(self):
        for url in ('/', '/contacts/', '/gallery/', '/feedback/', '/login/'):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, url)

    def test_manage_requires_login(self):
        response = self.client.get('/manage/pages/')
        self.assertEqual(response.status_code, 302)


class FeedbackTests(TestCase):
    def test_feedback_is_saved(self):
        response = self.client.post('/feedback/', {
            'name': 'Иван',
            'email': 'ivan@example.com',
            'phone': '+7 900 000-00-00',
            'message': 'Нужно ТО гирбокса V2',
        })
        self.assertEqual(response.status_code, 302)
        message = FeedbackMessage.objects.get(email='ivan@example.com')
        self.assertEqual(message.name, 'Иван')
        self.assertFalse(message.is_read)


class SchedulerTests(TestCase):
    def test_daily_job_reminds_and_deletes_old_read_messages(self):
        old = FeedbackMessage.objects.create(
            name='Старая заявка',
            email='old@example.com',
            message='Уже прочитано',
            is_read=True,
        )
        FeedbackMessage.objects.filter(pk=old.pk).update(
            created_at=timezone.now() - timedelta(days=40)
        )
        fresh = FeedbackMessage.objects.create(
            name='Пётр',
            email='petr@example.com',
            message='Свежая прочитанная заявка',
            is_read=True,
        )

        reminder, deleted = run_scheduled_jobs()
        again, _deleted_again = run_scheduled_jobs()

        self.assertEqual(reminder.pk, again.pk)
        self.assertEqual(DailyReminder.objects.count(), 1)
        self.assertEqual(reminder.day, timezone.localdate())
        self.assertIn('непрочитанных заявок', reminder.text)
        self.assertGreaterEqual(deleted, 1)
        self.assertFalse(FeedbackMessage.objects.filter(pk=old.pk).exists())
        self.assertTrue(FeedbackMessage.objects.filter(pk=fresh.pk).exists())


class CacheTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_menu_and_catalog_are_cached(self):
        with self.assertNumQueries(1):
            menu = get_menu_pages()
        with self.assertNumQueries(0):
            self.assertEqual(get_menu_pages(), menu)

        with self.assertNumQueries(2):
            catalog = get_public_catalog()
        with self.assertNumQueries(0):
            self.assertEqual(get_public_catalog(), catalog)
        self.assertIn('Главная', catalog['pages'])

    def test_home_data_is_faster_with_cache(self):
        result = benchmark_home(repeats=40)
        self.assertLess(result['warm_ms'], result['cold_ms'])
        self.assertGreater(result['faster'], 1)


class PageSlugTests(TestCase):
    def test_duplicate_title_gets_unique_slug(self):
        user = User.objects.create_user('editor', password='secret12')
        self.client.force_login(user)
        payload = {
            'title': 'Прайс',
            'subtitle': 'Стоимость работ',
            'content': 'Диагностика и ТО',
        }
        first = self.client.post('/manage/pages/new/', payload)
        second = self.client.post('/manage/pages/new/', payload)
        self.assertEqual(first.status_code, 302)
        self.assertEqual(second.status_code, 302)
        slugs = list(Page.objects.filter(title='Прайс').values_list('slug', flat=True))
        self.assertEqual(len(slugs), 2)
        self.assertEqual(len(set(slugs)), 2)
