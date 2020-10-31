from django.test import Client, TestCase
from cocktails.forms import CocktailForm
from products.models import Product, Category


class TestForms(TestCase):

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

    def test_cocktail_form_data_valid(self):
        self.form = CocktailForm(data={
            'name': "test_name",
            'product': self.test_product,
            'product_measure': "2 oz",
            'ingredient_1': "ingredient",
            'method': "stir",
        })

        self.assertTrue(self.form.is_valid())
        self.assertTrue(self.form.fields['name'].widget.attrs['placeholder'],
                        "Name")
        self.assertFalse(self.form.fields['name'].label)

    def test_cocktail_form_data_invalid(self):
        self.form = CocktailForm(data={
            'name': "test_name",
            'product': self.test_product,
            'product_measure': "2 oz",
            'ingredient_1': "ingredient",
        })

        self.assertFalse(self.form.is_valid())
