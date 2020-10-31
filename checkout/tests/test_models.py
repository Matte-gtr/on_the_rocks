from django.test import TestCase
from checkout.models import Order, OrderLineItem
from products.models import Product, Category


class TestModels(TestCase):

    def setUp(self):

        self.test_order = Order.objects.create(
            first_name="Dave",
            last_name="Smith",
            email="example@testing.com",
            contact_number="01234567",
            street_address1="4 Test road",
            town_or_city="Testington",
            country="GB",
            cart_contents="[{2,1},{27,2}",
            stripe_pid="gsd098gdf9g",
            shipping_cost=6.00,
            order_cost=24.50,
            grand_total=30.50
        )
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

    def test_order_creates_order_number(self):
        self.assertTrue(self.test_order.order_number)

    def check_order_cost_updates(self):
        self.test_order.order_number = "597384756CF54D51BD869685C5F06519"
        self.test_order_line_item = OrderLineItem.objects.create(
            order=self.test_order.order_number,
            product=self.test_product,
            quantity=1
        )
        self.assertEqual(self.test_order.order_cost, 25.50)
        self.assertEqual(self.test_order_line_item.lineitem_total, 25.50)
