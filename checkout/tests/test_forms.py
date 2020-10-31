from django.test import Client, TestCase
from checkout.forms import OrderForm


class TestForms(TestCase):

    def setUp(self):
        self.client = Client()

    def test_order_form_data_valid(self):
        self.form = OrderForm(data={
            'first_name': "Dave",
            'last_name': "Smith",
            'email': "example@testing.com",
            'contact_number': "01234567",
            'street_address1': "4 Test road",
            'town_or_city': "Testington",
            'country': "GB",
            'cart_contents': "[{2,1},{27,2}",
            'stripe_pid': "gsd098gdf9g",
            'shipping_cost': 6.00,
            'order_cost': 24.50,
            'grand_total': 30.50
        })

        self.assertTrue(self.form.is_valid())
        self.assertTrue(self.form.fields['first_name'].widget.
                        attrs['autofocus'])
        self.assertFalse(self.form.fields['first_name'].label)
