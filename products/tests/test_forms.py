from django.test import Client, TestCase
from products.forms import ProductForm
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

    def test_product_form_data_valid(self):
        self.form = ProductForm(data={
            'category': self.test_category,
            'name': "test_name1",
            'description': "test description",
            'size': "70cl",
            'proof': 40,
            'price': 25.50,
        })

        self.assertTrue(self.form.is_valid())
        self.assertTrue(self.form.fields['category'].
                        widget.attrs['placeholder'], "Category")
        self.assertTrue(self.form.fields['name'].widget.attrs['class'],
                        'user-profile-input')

    def test_product_form_data_invalid(self):
        self.form = ProductForm(data={
            'category': self.test_category,
            'name': "test_name1",
            'description': "test description",
            'size': "70cl",
            'proof': 40,
        })

        self.assertFalse(self.form.is_valid())
