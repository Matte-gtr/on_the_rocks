from django.shortcuts import render, redirect, reverse


def view_cart(request):
    """ Returns the shopping cart page page """
    template = 'cart/cart.html'
    context = {
        'page_header': 'Shopping Cart',
    }
    return render(request, template, context)


def add_to_cart(request, product_id):
    """ add a product/quantity to the cart """
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if product_id in list(cart.keys()):
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)


def update_quantity(request, product_id):
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    cart[product_id] = quantity

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def delete_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(product_id)
    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def add_crate_to_cart(request):
    """ add your custom crate to the cart """
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
    else:
        # messages(request, f'You only have {crate_count}
        # items in your crate.')
        return redirect(redirect_url)

    for key, value in cart.items():
        print(type(value))
        print(crate_count)
    print(cart)

    request.session['cart'] = cart
    request.session['crate'] = {}
    return redirect(redirect_url)
