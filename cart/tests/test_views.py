from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.view_cart_url = reverse('view_cart')

    def test_view_cart_view(self):
        response = self.client.get(self.view_cart_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')
