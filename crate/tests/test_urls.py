from django.test import SimpleTestCase
from django.urls import resolve, reverse
from crate.views import create_a_crate, add_to_crate,\
    delete_from_crate, empty_crate


class TestUrls(SimpleTestCase):

    def test_create_a_crate_url_resolved(self):
        url = reverse('create_a_crate')
        self.assertEqual(url, '/crate/')
        self.assertEqual(resolve(url).func, create_a_crate)

    def test_add_to_crate_url_resolved(self):
        url = reverse('add_to_crate', args=[2])
        self.assertEqual(url, '/crate/add_to_crate/2')
        self.assertEqual(resolve(url).func, add_to_crate)

    def test_delete_from_crate_url_resolved(self):
        url = reverse('delete_from_crate', args=[2])
        self.assertEqual(url, '/crate/delete_from_crate/2')
        self.assertEqual(resolve(url).func, delete_from_crate)

    def test_empty_crate_url_resolved(self):
        url = reverse('empty_crate')
        self.assertEqual(url, '/crate/empty_crate/')
        self.assertEqual(resolve(url).func, empty_crate)
