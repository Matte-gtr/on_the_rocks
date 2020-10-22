from django.shortcuts import get_object_or_404
from django.conf import settings
from products.models import Product
from decimal import Decimal


def cart_contents(request):
    products_in_cart = []
    crates_in_cart = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})

    for product_id, quantity in cart.items():
        if type(quantity) == int:
            product = get_object_or_404(Product, pk=product_id)
            total += quantity * product.price
            product_count += quantity
            products_in_cart.append({
                'product_id': product_id,
                'quantity': quantity,
                'product': product,
            })
        else:
            items = []
            original_price = 0
            discounted_price = 0
            for product_pk, amount in quantity.items():
                product = get_object_or_404(Product, pk=product_pk)
                original_price += amount * product.price
                discounted_price += (amount * product.price) * Decimal(0.8)
                discounted_product_price = product.price * Decimal(0.8)
                total += (amount * product.price) * Decimal(0.8)
                product_count += amount
                items.append({
                    'product_id': product_pk,
                    'quantity': amount,
                    'product': product,
                    'price': discounted_product_price,
                })
            crates_in_cart.append({
                'crate_id': product_id,
                'items': items,
                'original_price': original_price,
                'discounted_price': discounted_price,
            })

    if total < settings.FREE_SHIPPING_THRESHOLD:
        free_shipping_delta = settings.FREE_SHIPPING_THRESHOLD - total
        shipping = settings.STANDARD_SHIPPING_COST
    else:
        free_shipping_delta = 0
        shipping = 0

    grand_total = shipping + total

    context = {
        'products_in_cart': products_in_cart,
        'crates_in_cart': crates_in_cart,
        'total': total,
        'product_count': product_count,
        'free_shipping_delta': free_shipping_delta,
        'free_shipping_threshold': settings.FREE_SHIPPING_THRESHOLD,
        'shipping': shipping,
        'grand_total': grand_total,
    }
    return context
