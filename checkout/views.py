from django.shortcuts import render, redirect, reverse, get_object_or_404,\
    HttpResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from cart.contexts import cart_contents

import stripe
import json


def checkout(request):
    """ displays the checkout page and creates an
    order on successful completion of the order form """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'contact_number': request.POST['contact_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'postcode': request.POST['postcode'],
            'county': request.POST['county'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.cart_contents = json.dumps(cart)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.save()
            for object_id, item_data in cart.items():
                try:
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
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the items in your cart does not exist. Please contact \
                            us to resolve this issue"))
                    order.delete()
                    return redirect(reverse('view_cart'))
            request.session['save_details'] = 'save-details' in request.POST
            return redirect(reverse('successful_checkout',
                            args=[order.order_number]))
        else:
            messages.error(request, 'There was an issue with your Order Details.\
                Please check the form and re-submit')
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, 'Your cart is empty')
            return redirect(reverse('view_cart'))

        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe_currency = settings.STRIPE_CURRENCY
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=stripe_currency,
        )
        order_form = OrderForm()
        messages.info(request, "Please fill out the Billing/Delivery details \
            form to complete your order.")

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'page_header': 'Checkout',
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, template, context)


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_details': request.POST.get('save_details'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error('Your payment cannot be processed at \
            the moment. Please try again later.')
        return HttpResponse(content=e, status=400)


def successful_checkout(request, order_number):
    """ displays a page after a successful checkout and handles
    the saving the customers order form details """
    order = get_object_or_404(Order, order_number=order_number)

    cratelist = []
    for item in order.lineitems.all():
        if item.crate_id:
            if item.crate_id not in cratelist:
                cratelist.append(item.crate_id)

    save_details = request.session.get('save_details')
    messages.success(request, 'Your order has been processed')
    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/successful_checkout.html'
    context = {
        'order': order,
        'page_header': 'Order Received',
        'save_details': save_details,
        'cratelist': cratelist,
    }
    return render(request, template, context)


def login_prompt(request):
    """ displays the login prompt before checkout """
    template = 'checkout/login_prompt.html'
    context = {
        'page_header': 'Checkout Options',
    }
    return render(request, template, context)
