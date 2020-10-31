from django.test import TestCase
from products.models import Category


class TestModels(TestCase):

    def setUp(self):
        self.test_category = Category.objects.create(
            name="test_whiskey",
            friendly_name="Test Whiskey",
        )

    def test_category_get_friendly_name(self):
        self.assertEqual(self.test_category.get_friendly_name(),
                         "Test Whiskey")
