from django.shortcuts import render, redirect, reverse
from products.models import Product, Category


def create_a_crate(request):
    template = "crate/create_a_crate.html"
    all_categories = Category.objects.all()
    category = False
    products = Product.objects.all()
    categories = ''

    if request.method == 'GET':
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
            category = request.GET['category']

    context = {
        'all_categories': all_categories,
        'page_header': 'Create-a-crate',
        'categories': categories,
        'products': products,
        'category': category,
    }
    return render(request, template, context)


def add_to_crate(request, product_id):
    """ add a product to the crate """
    crate = request.session.get('crate', {})
    quantity = 1

    if product_id in list(crate.keys()):
        crate[product_id] += quantity
    else:
        crate[product_id] = quantity

    request.session['crate'] = crate
    return redirect(reverse('create_a_crate'))


def delete_from_crate(request, product_id):
    crate = request.session.get('crate', {})
    crate.pop(product_id)
    request.session['crate'] = crate
    return redirect(reverse('create_a_crate'))
