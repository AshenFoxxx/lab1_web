from django.test import TestCase


class SmokeTests(TestCase):
    def test_public_pages(self):
        for url in ('/', '/contacts/', '/gallery/', '/feedback/', '/login/'):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, url)

    def test_manage_requires_login(self):
        response = self.client.get('/manage/pages/')
        self.assertEqual(response.status_code, 302)
