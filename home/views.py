from django.shortcuts import render, get_object_or_404
from products.models import Product
from django.db.models import Count
from checkout.models import OrderLineItem


def index(request):
    """ Returns the index/home page """
    template = 'home/index.html'
    return render(request, template)


def about_us(request):
    """ a view to display the about us page """
    product_ids = OrderLineItem.objects.values_list('product').\
        annotate(product_count=Count('product')).order_by('product')[:6]

    if len(product_ids) < 6:
        popular_products = Product.objects.all()[:6]
    else:
        popular_products = []
        for key, value in product_ids:
            item = get_object_or_404(Product, pk=key)
            popular_products.append(item)

    template = 'home/about_us.html'
    context = {
        'page_header': 'About us',
        'products': popular_products,
    }
    return render(request, template, context)
