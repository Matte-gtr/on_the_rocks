from django.conf import settings


def cart_contents(request):
    cart_items = []
    total = 0
    product_count = 0

    if total < settings.FREE_SHIPPING_THRESHOLD:
        free_delivery_delta = settings.FREE_SHIPPING_THRESHOLD - total
    else:
        free_delivery_delta = 0

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'free_delivery_delta': free_delivery_delta,
    }
    return context
