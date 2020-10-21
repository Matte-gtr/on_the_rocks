from django.shortcuts import get_object_or_404
from products.models import Product


def crate_contents(request):
    products_in_crate = []
    crate_total = 0
    crate_product_count = 0
    crate = request.session.get('crate', {})
    category_selected = ''
    # products = Product.objects.all()

    for product_id, quantity in crate.items():
        product = get_object_or_404(Product, pk=product_id)
        crate_total += quantity * product.price
        crate_product_count += quantity
        category_selected = product.category
        products_in_crate.append({
            'product_id': product_id,
            'quantity': quantity,
            'product': product,
        })
        # products = products.filter(category__name__in=category_selected.name)

    context = {
        'products_in_crate': products_in_crate,
        'crate_total': crate_total,
        'crate_product_count': crate_product_count,
        'category_selected': category_selected,
    }
    return context
