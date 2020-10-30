from django.shortcuts import render, get_object_or_404
from products.models import Product
from django.db.models import Count
from checkout.models import OrderLineItem


def about_us(request):
    """ a view to display the about us page """
    product_ids = OrderLineItem.objects.values_list('product').\
        annotate(product_count=Count('product')).order_by('product')[:5]
    if len(product_ids) < 5:
        popular_products = Product.objects.all()[:5]
    else:
        popular_products = []
        for key, value in product_ids:
            popular_products.append(Product, pk=key)

    template = 'about_us/about_us.html'
    context = {
        'page_header': 'About us',
        'products': popular_products,
    }
    return render(request, template, context)
