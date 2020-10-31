from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.home_url = reverse('home')
        self.about_us_url = reverse('about_us')

    def test_home_view(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_about_us_view(self):
        response = self.client.get(self.about_us_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/about_us.html')
