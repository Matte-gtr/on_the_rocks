from django.http import HttpResponse
from .models import Order, OrderLineItem
from products.models import Product

import json
import time


class Stripe_WebHook_Handler:
    """ Handle stripe webhooks """

    def __init__(self, request):
        self.request = request

    def handle_payment_intent_succeeded(self, event):
        """ Handle Stripes payment intent succeeded webhook """
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        save_details = intent.metadata.save_details
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        for key, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[key] = None

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    first_name__iexact=shipping_details.name.split(' ')[0],
                    last_name__iexact=shipping_details.name.split(' ')[1],
                    email__iexact=billing_details.email,
                    contact_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    cart_contents=cart,
                    stripe_pid=pid,
                    grand_total=grand_total,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(content=f'Webhook recieved: {event["type"]}. \
                Order already exists in the database', status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    first_name=shipping_details.name.split(' ')[0],
                    last_name=shipping_details.name.split(' ')[1],
                    email=billing_details.email,
                    contact_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    cart_contents=cart,
                    stripe_pid=pid,
                )
                for object_id, item_data in json.loads(cart).items():
                    if isinstance(item_data, int):
                        product = Product.objects.get(id=object_id)
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for product_id, quantity in item_data.items():
                            product = Product.objects.get(id=product_id)
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                crate_id=object_id,
                                quantity=quantity,
                            )
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(status=500, content=f'Webhook recieved: \
                    {event["type"]} with error: {e}')
        return HttpResponse(content=f'Webhook recieved: {event["type"]}: Order \
            created in webhook', status=200)

    def handle_payment_intent_payment_failed(self, event):
        """ Handle Stripes payment intent payment failed webhook """
        return HttpResponse(content=f'Webhook recieved: {event["type"]}',
                            status=200)

    def handle_webhook(self, event):
        """ Handle Stripes unknown webhook """
        return HttpResponse(content=f'Unknown Webhook recieved: \
                            {event["type"]}', status=200)