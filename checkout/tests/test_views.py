from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.login_prompt_url = reverse('login_prompt')

    def test_login_prompt_view(self):
        response = self.client.get(self.login_prompt_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/login_prompt.html')
