from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your cart is empty')
        return redirect(reverse('view_cart'))

    messages.info(request, "Please fill out the Billing/Delivery details \
        form to complete your order.")
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'page_header': 'Checkout',
        'stripe_public_key': 'pk_test_51HUHJdBjaSvU6yf88OBQWOTgUft887PMgMCJP5E8y4PSMxqIduVBvYkbYkKlMjkQpJ8dUg0KzyFcpClVhatbxeuJ00xXJYLl9h',
        'client_secret': 'test client secret',
    }
    return render(request, template, context)
