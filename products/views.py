from django.shortcuts import render, redirect, reverse
from .models import Product
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage


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

    pagi = Paginator(products, 36)
    page_num = request.GET.get('page', 1)
    try:
        page = pagi.page(page_num)
    except EmptyPage:
        page = pagi.page(1)

    context = {
        'products': page,
        'page_header': "Whiskeys"
    }

    return render(request, template, context)
