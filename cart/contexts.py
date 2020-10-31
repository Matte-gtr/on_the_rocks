from django.shortcuts import get_object_or_404
from django.conf import settings
from products.models import Product
from decimal import Decimal


def cart_contents(request):
    """ returns information based on the products in the cart """
    products_in_cart = []
    crates_in_cart = []
    total = 0
    product_count = 0
    item_count = 0
    cart = request.session.get('cart', {})

    for object_id, item_data in cart.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=object_id)
            total += item_data * product.price
            product_count += item_data
            item_count += item_data
            products_in_cart.append({
                'product_id': object_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            items = []
            product_count += 1
            original_price = 0
            discounted_price = 0
            for product_id, quantity in item_data.items():
                product = get_object_or_404(Product, pk=product_id)
                original_price += quantity * product.price
                discounted_price += (quantity * product.price) * Decimal(0.8)
                discounted_product_price = product.price * Decimal(0.8)
                total += (quantity * product.price) * Decimal(0.8)
                item_count += quantity
                items.append({
                    'product_id': product_id,
                    'quantity': quantity,
                    'product': product,
                    'price': discounted_product_price,
                })
            crates_in_cart.append({
                'crate_id': object_id,
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
        'item_count': item_count,
        'free_shipping_delta': free_shipping_delta,
        'free_shipping_threshold': settings.FREE_SHIPPING_THRESHOLD,
        'shipping': shipping,
        'grand_total': grand_total,
    }
    return context
