from django.test import SimpleTestCase
from django.urls import resolve, reverse
from cart.views import view_cart, add_to_cart, update_quantity,\
    delete_from_cart, add_crate_to_cart, delete_crate_from_cart


class TestUrls(SimpleTestCase):

    def test_view_cart_url_resolved(self):
        url = reverse('view_cart')
        self.assertEqual(url, '/cart/')
        self.assertEqual(resolve(url).func, view_cart)

    def test_add_to_cart_url_resolved(self):
        url = reverse('add_to_cart', args=[2])
        self.assertEqual(url, '/cart/add_to_cart/2')
        self.assertEqual(resolve(url).func, add_to_cart)

    def test_update_quantity_data_url_resolved(self):
        url = reverse('update_quantity', args=[2])
        self.assertEqual(url, '/cart/update_quantity/2')
        self.assertEqual(resolve(url).func, update_quantity)

    def test_delete_from_cart_url_resolved(self):
        url = reverse('delete_from_cart', args=[2])
        self.assertEqual(url, '/cart/delete_from_cart/2')
        self.assertEqual(resolve(url).func, delete_from_cart)

    def test_add_crate_to_cart_url_resolved(self):
        url = reverse('add_crate_to_cart')
        self.assertEqual(url, '/cart/add_crate_to_cart/')
        self.assertEqual(resolve(url).func, add_crate_to_cart)

    def test_delete_crate_from_cart_url_resolved(self):
        url = reverse('delete_crate_from_cart', args=[2])
        self.assertEqual(url, '/cart/delete_crate_from_cart/2')
        self.assertEqual(resolve(url).func, delete_crate_from_cart)
