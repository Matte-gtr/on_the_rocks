from django.shortcuts import render, get_object_or_404
from products.models import Product
from django.db.models import Count
from checkout.models import OrderLineItem


def about_us(request):
    """ a view to display the about us page """
    first_product_id = OrderLineItem.objects.values_list('product').\
        annotate(product_count=Count('product')).order_by('product')[:1]
    product_ids = OrderLineItem.objects.values_list('product').\
        annotate(product_count=Count('product')).order_by('product')[1:6]

    if len(product_ids) < 3:
        popular_products = Product.objects.all()[1:6]
        first_product = Product.objects.all()[:1][0]
    else:
        popular_products = []
        for key, value in product_ids:
            item = get_object_or_404(Product, pk=key)
            popular_products.append(item)
            first_product = get_object_or_404(Product,
                                              pk=first_product_id[0][0])

    template = 'about_us/about_us.html'
    context = {
        'page_header': 'About us',
        'products': popular_products,
        'first_product': first_product,
    }
    return render(request, template, context)
