from django.shortcuts import render, redirect, reverse
from .models import Product
from django.contrib import messages
from django.db.models import Q


def products(request):
    """ Returns a list of products """

    products = Product.objects.all()

    if request.GET:
        if "search" in request.GET:
            query = request.GET.get('search')
            if not query:
                messages(request, "No search term entered")
                return redirect(reverse('products'))
            search_results = Q(name__icontains=query) |\
                Q(description__icontains=query) |\
                Q(detail__icontains=query)
            products = products.filter(search_results)

    template = 'products/products.html'

    context = {
        'products': products,
        'page_header': "Whiskeys"
    }

    return render(request, template, context)
