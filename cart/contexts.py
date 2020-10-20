from django.shortcuts import get_object_or_404
from django.conf import settings
from products.models import Product


def cart_contents(request):
    products_in_cart = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})
    for product_id, quantity in cart.items():
        # if product is not a crate...
        product = get_object_or_404(Product, pk=product_id)
        total += quantity * product.price
        product_count += quantity
        products_in_cart.append({
            'product_id': product_id,
            'quantity': quantity,
            'product': product,
        })

    if total < settings.FREE_SHIPPING_THRESHOLD:
        free_delivery_delta = settings.FREE_SHIPPING_THRESHOLD - total
    else:
        free_delivery_delta = 0

    context = {
        'products_in_cart': products_in_cart,
        'total': total,
        'product_count': product_count,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_SHIPPING_THRESHOLD,
    }
    return context
