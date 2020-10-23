from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from products.models import Product


def view_cart(request):
    """ Returns the shopping cart page page """
    template = 'cart/cart.html'
    context = {
        'page_header': 'Shopping Cart',
    }
    return render(request, template, context)


def add_to_cart(request, product_id):
    """ add a product/quantity to the cart """
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if product_id in list(cart.keys()):
        cart[product_id] += quantity
        messages.success(request, f'{product.name} quantity has been \
            adjusted to {cart[product_id]} in your cart', extra_tags='cart')
    else:
        cart[product_id] = quantity
        messages.success(request, f'{product.name} has been added to \
            your cart', extra_tags='cart')

    request.session['cart'] = cart
    return redirect(redirect_url)


def update_quantity(request, product_id):
    """ updates the quantity of a selected item in the cart """
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    cart[product_id] = quantity
    messages.success(request, f'{product.name} quantity has been \
            adjusted to {cart[product_id]}')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def delete_from_cart(request, product_id):
    """ deletes an item from the cart """
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})
    try:
        cart.pop(product_id)
        messages.success(request, f'{product.name} has been removed \
            from your cart')
        request.session['cart'] = cart
    except Exception as e:
        messages.error(request, f'Error deleting product: {e}')

    return redirect(reverse('view_cart'))


def add_crate_to_cart(request):
    """ add your custom crate to the cart """
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})
    crate = request.session.get('crate')
    count_check = 0
    crate_count = 1

    try:
        for product_id in list(crate.keys()):
            count_check += crate[product_id]

        if count_check == 6:
            while f'crate{crate_count}' in list(cart.keys()):
                crate_count += 1
            cart[f'crate{crate_count}'] = crate
            messages.success(request, 'Your custom crate has been \
                added to your cart', extra_tags='cart')
        else:
            messages.warning(request, f'You only have {crate_count} \
                items in your crate.')
            return redirect(redirect_url)
    except Exception as e:
        messages.error(request, f'Error adding crate to cart: {e}')

    request.session['cart'] = cart
    request.session['crate'] = {}
    return redirect(redirect_url)


def delete_crate_from_cart(request, product_id):
    """ deletes a crate from the cart """
    cart = request.session.get('cart', {})
    try:
        cart.pop(product_id)
        messages.success(request, 'Your custom crate has been removed \
            from your cart')
        request.session['cart'] = cart
    except Exception as e:
        messages.error(request, f'Error deleting crate: {e}')

    return redirect(reverse('view_cart'))
