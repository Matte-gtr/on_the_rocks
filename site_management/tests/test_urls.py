from django.test import SimpleTestCase
from django.urls import resolve, reverse
from site_management.views import site_management, approve_review,\
    delete_review, user_profile, order_history


class TestUrls(SimpleTestCase):

    def test_site_management_url_resolved(self):
        url = reverse('site_management')
        self.assertEqual(url, '/site_management/')
        self.assertEqual(resolve(url).func, site_management)

    def test_approve_review_url_resolved(self):
        url = reverse('approve_review', args=[2])
        self.assertEqual(url, '/site_management/approve_review/2/')
        self.assertEqual(resolve(url).func, approve_review)

    def test_delete_review_url_resolved(self):
        url = reverse('delete_review', args=[2])
        self.assertEqual(url, '/site_management/delete_review/2/')
        self.assertEqual(resolve(url).func, delete_review)

    def test_user_profile_url_resolved(self):
        url = reverse('user_profile', args=["Dave23"])
        self.assertEqual(url, '/site_management/user_profile/Dave23/')
        self.assertEqual(resolve(url).func, user_profile)

    def test_order_history_url_resolved(self):
        url = reverse('order_history', args=["2d456tsd"])
        self.assertEqual(url, '/site_management/order_history/2d456tsd/')
        self.assertEqual(resolve(url).func, order_history)
