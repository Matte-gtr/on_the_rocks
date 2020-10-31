from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from products.models import Product, Category


def create_a_crate(request):
    """ a view to return the create a crate page """
    template = "crate/create_a_crate.html"
    all_categories = Category.objects.all()
    category = False
    products = Product.objects.all()
    categories = None
    crate = request.session.get('crate', {})
    if crate.items():
        for product_id, quantity in crate.items():
            product = get_object_or_404(Product, pk=product_id)
            categories = product.category.name.split(',')
            products = products.filter(category__name__in=categories)

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
    """ a view to add a product to the crate """
    product = get_object_or_404(Product, pk=product_id)
    crate = request.session.get('crate', {})
    quantity = int(request.POST.get('quantity'))

    if product_id in list(crate.keys()):
        crate[product_id] += quantity
        messages.success(request, f'{product.name} quantity has been \
            adjusted to {crate[product_id]}', extra_tags='crate')
    else:
        crate[product_id] = quantity
        messages.success(request, f'{product.name} has been added to \
            your crate', extra_tags='crate')

    request.session['crate'] = crate
    return redirect(reverse('create_a_crate'))


def delete_from_crate(request, product_id):
    """ a view to delete a product from the crate """
    product = get_object_or_404(Product, pk=product_id)
    crate = request.session.get('crate', {})
    quantity = 1

    if product_id in list(crate.keys()):
        if crate[product_id] > 1:
            crate[product_id] -= quantity
            messages.success(request, f'{product.name} quantity has been \
            adjusted to {crate[product_id]} in your crate', extra_tags='crate')
        else:
            crate.pop(product_id)
            messages.success(request, f'{product.name} has been removed from \
            your crate', extra_tags='crate')

    request.session['crate'] = crate
    return redirect(reverse('create_a_crate'))


def empty_crate(request):
    """ a view to empty the crate """
    request.session['crate'] = {}
    messages.success(request, 'Your crate has been emptied')

    return redirect(reverse('create_a_crate'))
