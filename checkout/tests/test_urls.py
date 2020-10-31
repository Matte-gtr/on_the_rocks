from django.test import SimpleTestCase
from django.urls import resolve, reverse
from checkout.views import checkout, cache_checkout_data, \
    successful_checkout, login_prompt


class TestUrls(SimpleTestCase):

    def test_login_prompt_url_resolved(self):
        url = reverse('login_prompt')
        self.assertEqual(url, '/checkout/login_prompt/')
        self.assertEqual(resolve(url).func, login_prompt)

    def test_checkout_url_resolved(self):
        url = reverse('checkout')
        self.assertEqual(url, '/checkout/')
        self.assertEqual(resolve(url).func, checkout)

    def test_cache_checkout_data_url_resolved(self):
        url = reverse('cache_checkout_data')
        self.assertEqual(url, '/checkout/cache_checkout_data/')
        self.assertEqual(resolve(url).func, cache_checkout_data)

    def test_successful_checkout_url_resolved(self):
        url = reverse('successful_checkout', args=[2])
        self.assertEqual(url, '/checkout/successful_checkout/2')
        self.assertEqual(resolve(url).func, successful_checkout)
