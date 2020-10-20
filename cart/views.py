from django.shortcuts import render, redirect


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
