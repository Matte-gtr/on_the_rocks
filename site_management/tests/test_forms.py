from django.test import Client, TestCase
from site_management.forms import ReviewForm, UserProfileForm
from django.contrib.auth.models import User


class TestForms(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create(
            username='tester',
            password="Lkjsdf98fsdf67",
            email='example@testing.com',
        )

    def test_review_form_data_valid(self):
        self.form = ReviewForm(data={
            'stars': 4,
            'review': "Good",
            'anon': False,
        })

        self.assertTrue(self.form.is_valid())
        self.assertTrue(self.form.fields['review'].label, "Review")

    def test_review_form_data_invalid(self):
        self.form = ReviewForm(data={
            'review': "Good",
            'anon': False,
        })

        self.assertFalse(self.form.is_valid())

    def test_user_profile_form_data_valid(self):
        self.form = UserProfileForm(data={
            'user': self.test_user,
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'example@testing.com',
        })

        self.assertTrue(self.form.is_valid())
