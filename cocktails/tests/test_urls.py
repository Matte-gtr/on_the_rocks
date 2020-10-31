from django.test import SimpleTestCase
from django.urls import resolve, reverse
from cocktails.views import cocktails, display_cocktail, delete_cocktail,\
    add_cocktail, edit_cocktail


class TestUrls(SimpleTestCase):

    def test_cocktails_url_resolved(self):
        url = reverse('cocktails')
        self.assertEqual(url, '/cocktails/')
        self.assertEqual(resolve(url).func, cocktails)

    def test_display_cocktail_url_resolved(self):
        url = reverse('display_cocktail', args=[2])
        self.assertEqual(url, '/cocktails/display_cocktail/2')
        self.assertEqual(resolve(url).func, display_cocktail)

    def test_delete_cocktail_url_resolved(self):
        url = reverse('delete_cocktail', args=[2])
        self.assertEqual(url, '/cocktails/delete_cocktail/2')
        self.assertEqual(resolve(url).func, delete_cocktail)

    def test_add_cocktail_url_resolved(self):
        url = reverse('add_cocktail')
        self.assertEqual(url, '/cocktails/add_cocktail/')
        self.assertEqual(resolve(url).func, add_cocktail)

    def test_edit_cocktail_url_resolved(self):
        url = reverse('edit_cocktail', args=[2])
        self.assertEqual(url, '/cocktails/edit_cocktail/2')
        self.assertEqual(resolve(url).func, edit_cocktail)
