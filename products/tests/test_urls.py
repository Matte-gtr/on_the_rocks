from django.test import SimpleTestCase
from django.urls import resolve, reverse
from products.views import products, product_display, add_product,\
    edit_product, delete_product


class TestUrls(SimpleTestCase):

    def test_products_url_resolved(self):
        url = reverse('products')
        self.assertEqual(url, '/products/')
        self.assertEqual(resolve(url).func, products)

    def test_product_display_url_resolved(self):
        url = reverse('product_display', args=[2])
        self.assertEqual(url, '/products/2/')
        self.assertEqual(resolve(url).func, product_display)

    def test_add_product_url_resolved(self):
        url = reverse('add_product')
        self.assertEqual(url, '/products/add_product/')
        self.assertEqual(resolve(url).func, add_product)

    def test_edit_product_url_resolved(self):
        url = reverse('edit_product', args=[2])
        self.assertEqual(url, '/products/edit_product/2')
        self.assertEqual(resolve(url).func, edit_product)

    def test_delete_product_url_resolved(self):
        url = reverse('delete_product', args=[2])
        self.assertEqual(url, '/products/delete_product/2')
        self.assertEqual(resolve(url).func, delete_product)
