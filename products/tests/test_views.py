from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product, Category


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_category = Category.objects.create(
            pk=1,
            name="test_name",
            friendly_name="Test Name",
        )
        self.test_product = Product.objects.create(
            pk=1,
            category=self.test_category,
            name="test_name1",
            description="test description",
            size="70cl",
            proof=40,
            price=25.50,
        )

        self.products_url = reverse('products')
        self.product_display_url = reverse('product_display',
                                           args=[self.test_product.id])

    def test_products_view(self):
        response = self.client.get(self.products_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_product_display_view(self):
        response = self.client.get(self.product_display_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_display.html')
