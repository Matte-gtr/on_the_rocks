import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from products.models import Product


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    contact_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    country = models.CharField(max_length=40, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    shipping_cost = models.DecimalField(max_digits=5, decimal_places=2,
                                        null=False, default=0)
    order_cost = models.DecimalField(max_digits=7, decimal_places=2,
                                     null=False, default=0)
    grand_total = models.DecimalField(max_digits=7, decimal_places=2,
                                      null=False, default=0)

    def _create_order_number(self):
        """ creates a unique order number for each order """
        return uuid.uuid4().hex.upper()

    def update_order_cost(self):
        """ Updates the grand total each time an order line item is added and
        calculates the delivery cost """
        self.order_cost = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_cost < settings.FREE_SHIPPING_THRESHOLD:
            self.shipping_cost = settings.STANDARD_SHIPPING_COST
            self.save
        else:
            self.shipping_cost = 0
        self.grand_total = self.order_cost + self.shipping_cost
        self.save()

    def save(self, *args, **kwargs):
        """ change defalt save method to create an order number if
        one doesn't already exist """
        if not self.order_number:
            self.order_number = self._create_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False,
                                on_delete=models.CASCADE)
    crate_id = models.CharField(max_length=10, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=7, decimal_places=2)

    def save(self, *args, **kwargs):
        """ change defalt save method to calculate the cost of
        each line item """
        if self.crate_id:
            self.lineitem_total = (self.product.price * self.quantity) * 0.8
        else:
            self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Product {self.product.id} on order {self.order_number}'
