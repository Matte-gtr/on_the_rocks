from django.test import SimpleTestCase
from django.urls import resolve, reverse
from home.views import index, about_us


class TestUrls(SimpleTestCase):

    def test_home_url_resolved(self):
        url = resolve('/')
        self.assertEqual(url.func, index)

    def test_about_us_url_resolved(self):
        url = reverse('about_us')
        self.assertEqual(url, '/about_us/')
        self.assertEqual(resolve(url).func, about_us)
