from django.shortcuts import render, redirect, reverse, get_object_or_404
from products.models import Product, Category


def create_a_crate(request):
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
    """ add a product to the crate """
    crate = request.session.get('crate', {})
    quantity = int(request.POST.get('quantity'))

    if product_id in list(crate.keys()):
        crate[product_id] += quantity
    else:
        crate[product_id] = quantity

    request.session['crate'] = crate
    return redirect(reverse('create_a_crate'))


def delete_from_crate(request, product_id):
    crate = request.session.get('crate', {})
    quantity = 1

    if product_id in list(crate.keys()):
        if crate[product_id] > 1:
            crate[product_id] -= quantity
        else:
            crate.pop(product_id)

    request.session['crate'] = crate
    return redirect(reverse('create_a_crate'))


def empty_crate(request):
    request.session['crate'] = {}

    return redirect(reverse('create_a_crate'))


def add_crate_to_cart(request):
    """ add your crate/quantity to the cart """
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})
    crate = request.session.get('crate')
    count_check = 0
    crate_count = 1

    for product_id in list(crate.keys()):
        count_check += crate[product_id]

    if count_check == 6:
        while f'crate{crate_count}' in list(cart.keys()):
            crate_count += 1
        cart[f'crate{crate_count}'] = crate

    for key, value in cart.items():
        print(type(value))
        print(crate_count)
    print(cart)

    request.session['cart'] = cart
    request.session['crate'] = {}
    return redirect(redirect_url)
