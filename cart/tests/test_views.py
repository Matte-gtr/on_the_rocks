from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.view_cart_url = reverse('view_cart')
        self.add_cart_url = reverse('add_to_cart', args=[2])
        self.update_q_url = reverse('update_quantity', args=[2])
        self.del_cart_url = reverse('delete_from_cart', args=[2])
        self.add_crate_url = reverse('add_crate_to_cart')
        self.del_crate_url = reverse('delete_crate_from_cart', args=['crate1'])
        self.redirect_url = 'reverse('product_display', args=[2])'

    def test_view_cart_view(self):
        response = self.client.get(self.view_cart_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')

    def test_add_to_cart_view(self):

        response = self.client.get(self.add_cart_url)

        # self.assertEquals(response.status_code, 302)
        # self.assertTemplateUsed(response, 'cart/cart.html')
