from django.shortcuts import get_object_or_404
from django.conf import settings
from products.models import Product


def cart_contents(request):
    products_in_cart = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})

    # if product is not a crate...
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        total += quantity * product.price
        product_count += quantity
        products_in_cart.append({
            'product_id': product_id,
            'quantity': quantity,
            'product': product,
        })
        # elif product is a crate...
            # do some other stuff to add the crate to the cart

    if total < settings.FREE_SHIPPING_THRESHOLD:
        free_shipping_delta = settings.FREE_SHIPPING_THRESHOLD - total
        shipping = settings.STANDARD_SHIPPING_COST
    else:
        free_shipping_delta = 0
        shipping = 0

    grand_total = shipping + total

    context = {
        'products_in_cart': products_in_cart,
        'total': total,
        'product_count': product_count,
        'free_shipping_delta': free_shipping_delta,
        'free_shipping_threshold': settings.FREE_SHIPPING_THRESHOLD,
        'shipping': shipping,
        'grand_total': grand_total,
    }
    return context
