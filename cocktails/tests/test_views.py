from django.test import TestCase, Client
from django.urls import reverse
from cocktails.models import Cocktail
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
        self.test_cocktail = Cocktail.objects.create(
            pk=1,
            name="test_name2",
            product=self.test_product,
            product_measure="2 oz",
            ingredient_1="ingredient",
            method="stir",
        )

        self.cocktails_url = reverse('cocktails')
        self.display_cocktail_url = reverse('display_cocktail',
                                            args=[self.test_cocktail.id])

    def test_cocktails_view(self):
        response = self.client.get(self.cocktails_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cocktails/cocktails.html')

    def test_display_cocktail_view(self):
        response = self.client.get(self.display_cocktail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cocktails/display_cocktail.html')
