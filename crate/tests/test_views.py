from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.create_a_crate_url = reverse('create_a_crate')

    def test_create_a_crate_view(self):
        response = self.client.get(self.create_a_crate_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'crate/create_a_crate.html')
